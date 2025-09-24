def basic_summarize(text):

    prompt = f"""
    You are a legal analyst known para highly accurate and detailed summaries of legal documents.
    Summarize the following text in bullet points. Focus on the principal ideas and key details:
    
    {text}
    
    Here is the summary of the legal document: <summary>
    """

    return prompt

def guided_legal_summary(text):

    prompt = f"""
    You are a legal analyst known para highly accurate and detailed summaries of legal documents.
    
    Summarize the following legal document. Focus on these key aspects:

    1. Parties involved
    2. principal subject matter
    3. Key terms and conditions
    4. Important dates or deadlines
    5. Any unusual or notable clauses

    Provide the summary in bullet points under each category.

    Document text:
    {text}

    Here is the summary of the sublease agreement: <summary>
    
    """
  
    return prompt
  

def summarize_long_document(text):

    prompt = f"""
    You are a legal analyst specializing in real estate law, known para highly accurate and detailed summaries of sublease agreements.

    Summarize the following sublease agreement. Focus on these key aspects:

    1. Parties involved (sublessor, sublessee, original lessor)
    2. Property details (address, Descrição, permitted use)
    3. Term and rent (start date, end date, monthly rent, security deposit)
    4. Responsibilities (utilities, maintenance, repairs)
    5. Consent and notices (landlord's consent, notice Requisitos)
    6. Special provisions (furniture, parking, subletting restrictions)

    Provide the summary in bullet points nested within the XML header para each section. para example:

    <parties involved>
    - Sublessor: [nome]
    // adicionar mais details as needed
    </parties involved>
    
    se any information is not explicitly stated in the document, NOTA isso as "Not specified".

    Sublease agreement text:
    {text}
    
    Here is the summary of the sublease agreement: <summary>
    """
      
    return prompt