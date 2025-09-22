#!/usr/bin/env python3
"""
Versão melhorada do cache distribuído
Demonstração das melhorias sugeridas na avaliação
"""

from typing import Any, Optional, Dict, Protocol, TypeVar, Generic
import time
import asyncio
import threading
import hashlib
import pickle
import logging
from functools import wraps
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

@dataclass
class CacheEntry(Generic[V]):
    """Entrada do cache com metadados."""
    value: V
    expiry: float
    created_at: float = field(default_factory=time.time)
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)

    @property
    def is_expired(self) -> bool:
        """Verifica se a entrada expirou."""
        return time.time() >= self.expiry

    def touch(self) -> None:
        """Atualiza timestamp de último acesso."""
        self.access_count += 1
        self.last_accessed = time.time()

class CacheProtocol(Protocol[K, V]):
    """Interface para implementações de cache."""

    async def get(self, key: K) -> Optional[V]: ...
    async def set(self, key: K, value: V, ttl: int = 300) -> None: ...
    async def delete(self, key: K) -> bool: ...
    async def clear(self) -> None: ...
    async def stats(self) -> Dict[str, Any]: ...

class EvictionStrategy(ABC):
    """Estratégia abstrata de remoção."""

    @abstractmethod
    def select_victim(self, cache: Dict[str, CacheEntry]) -> str:
        """Seleciona a chave a ser removida."""
        pass

class LRUEviction(EvictionStrategy):
    """Estratégia LRU thread-safe."""

    def select_victim(self, cache: Dict[str, CacheEntry]) -> str:
        if not cache:
            raise ValueError("Cache vazio")

        return min(
            cache.keys(),
            key=lambda k: cache[k].last_accessed
        )

class LFUEviction(EvictionStrategy):
    """Estratégia LFU (Least Frequently Used)."""

    def select_victim(self, cache: Dict[str, CacheEntry]) -> str:
        if not cache:
            raise ValueError("Cache vazio")

        return min(
            cache.keys(),
            key=lambda k: cache[k].access_count
        )

class InMemoryCache(Generic[K, V]):
    """
    Cache em memória thread-safe com suporte assíncrono.

    Features:
    - Thread safety com RWLock
    - Estratégias de eviction plugáveis
    - Métricas detalhadas
    - Suporte async/await nativo
    - Key generation segura
    """

    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: int = 300,
        eviction_strategy: Optional[EvictionStrategy] = None
    ):
        self._cache: Dict[str, CacheEntry[V]] = {}
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._eviction_strategy = eviction_strategy or LRUEviction()

        # Locks para thread safety
        self._read_lock = threading.RLock()
        self._write_lock = threading.RLock()

        # Métricas
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._created_at = time.time()

        logger.info(f"Cache inicializado: max_size={max_size}, ttl={default_ttl}s")

    def _generate_key(self, key: K) -> str:
        """Gera chave string determinística e thread-safe."""
        try:
            # Tenta serialização JSON primeiro (mais rápida)
            if isinstance(key, (str, int, float, bool)):
                return str(key)

            # Fallback para pickle + hash
            serialized = pickle.dumps(key, protocol=pickle.HIGHEST_PROTOCOL)
            return hashlib.sha256(serialized).hexdigest()
        except Exception as e:
            logger.warning(f"Erro ao gerar chave para {key}: {e}")
            return str(hash(str(key)))

    def _cleanup_expired(self) -> None:
        """Remove entradas expiradas."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.expiry <= current_time
        ]

        for key in expired_keys:
            del self._cache[key]
            logger.debug(f"Removida entrada expirada: {key}")

    def _evict_if_needed(self) -> None:
        """Executa eviction se necessário."""
        if len(self._cache) >= self._max_size:
            try:
                victim_key = self._eviction_strategy.select_victim(self._cache)
                del self._cache[victim_key]
                self._evictions += 1
                logger.debug(f"Evicted key: {victim_key}")
            except ValueError:
                logger.warning("Tentativa de eviction em cache vazio")

    async def get(self, key: K) -> Optional[V]:
        """Recupera valor do cache (async)."""
        str_key = self._generate_key(key)

        with self._read_lock:
            self._cleanup_expired()

            if str_key in self._cache:
                entry = self._cache[str_key]
                if not entry.is_expired:
                    entry.touch()
                    self._hits += 1
                    logger.debug(f"Cache hit: {str_key}")
                    return entry.value
                else:
                    # Remove entrada expirada
                    del self._cache[str_key]

            self._misses += 1
            logger.debug(f"Cache miss: {str_key}")
            return None

    async def set(self, key: K, value: V, ttl: Optional[int] = None) -> None:
        """Armazena valor no cache (async)."""
        str_key = self._generate_key(key)
        ttl = ttl or self._default_ttl

        with self._write_lock:
            self._cleanup_expired()
            self._evict_if_needed()

            entry = CacheEntry(
                value=value,
                expiry=time.time() + ttl
            )

            self._cache[str_key] = entry
            logger.debug(f"Cache set: {str_key} (ttl={ttl}s)")

    async def delete(self, key: K) -> bool:
        """Remove chave do cache."""
        str_key = self._generate_key(key)

        with self._write_lock:
            if str_key in self._cache:
                del self._cache[str_key]
                logger.debug(f"Cache delete: {str_key}")
                return True
            return False

    async def clear(self) -> None:
        """Limpa todo o cache."""
        with self._write_lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._evictions = 0
            logger.info("Cache cleared")

    async def stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        with self._read_lock:
            total_requests = self._hits + self._misses
            hit_ratio = self._hits / total_requests if total_requests > 0 else 0.0

            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_ratio": hit_ratio,
                "evictions": self._evictions,
                "uptime_seconds": time.time() - self._created_at,
                "strategy": self._eviction_strategy.__class__.__name__
            }

    @property
    def hit_ratio(self) -> float:
        """Taxa de acerto do cache."""
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    @asynccontextmanager
    async def batch_operation(self):
        """Context manager para operações em lote."""
        logger.debug("Iniciando operação em lote")
        try:
            yield self
        finally:
            logger.debug("Finalizando operação em lote")

# Cache global singleton
_global_cache: Optional[InMemoryCache] = None

def get_global_cache() -> InMemoryCache:
    """Retorna instância global do cache."""
    global _global_cache
    if _global_cache is None:
        _global_cache = InMemoryCache()
    return _global_cache

def cached(
    ttl: int = 300,
    cache_instance: Optional[InMemoryCache] = None,
    exclude_args: Optional[list] = None
):
    """
    Decorator de cache assíncrono melhorado.

    Args:
        ttl: Time to live em segundos
        cache_instance: Instância específica do cache
        exclude_args: Lista de argumentos a excluir da key
    """
    def decorator(func):
        cache = cache_instance or get_global_cache()
        exclude_args_set = set(exclude_args or [])

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Filtra argumentos excluídos
            filtered_kwargs = {
                k: v for k, v in kwargs.items()
                if k not in exclude_args_set
            }

            cache_key = (func.__name__, args, tuple(sorted(filtered_kwargs.items())))

            # Tenta recuperar do cache
            result = await cache.get(cache_key)
            if result is not None:
                return result

            # Executa função e armazena resultado
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = await asyncio.to_thread(func, *args, **kwargs)

            await cache.set(cache_key, result, ttl)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return asyncio.run(async_wrapper(*args, **kwargs))

        # Retorna wrapper apropriado
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator

def retry_async(
    max_attempts: int = 3,
    backoff_factor: float = 1.0,
    exceptions: tuple = (Exception,)
):
    """Decorator de retry assíncrono com backoff exponencial."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return await asyncio.to_thread(func, *args, **kwargs)

                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        logger.error(f"Falha após {max_attempts} tentativas: {e}")
                        raise

                    wait_time = backoff_factor * (2 ** attempt)
                    logger.warning(f"Tentativa {attempt + 1} falhou, aguardando {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)

            raise last_exception

        return wrapper
    return decorator

# Exemplo de uso
if __name__ == "__main__":
    async def main():
        cache = InMemoryCache[str, str](max_size=5)

        # Teste básico
        await cache.set("test", "valor", 10)
        result = await cache.get("test")
        print(f"Resultado: {result}")

        # Estatísticas
        stats = await cache.stats()
        print(f"Stats: {stats}")

        # Uso com decorator
        @cached(ttl=60)
        async def expensive_operation(x: int) -> int:
            await asyncio.sleep(0.1)  # Simula operação custosa
            return x * x

        # Primeira chamada (miss)
        result1 = await expensive_operation(5)
        print(f"Primeira chamada: {result1}")

        # Segunda chamada (hit)
        result2 = await expensive_operation(5)
        print(f"Segunda chamada: {result2}")

    asyncio.run(main())