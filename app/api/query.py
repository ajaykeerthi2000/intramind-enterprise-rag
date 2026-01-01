import time
from fastapi import APIRouter, Depends
from app.schemas.query import QueryRequest, QueryResponse
from app.security.jwt_auth import verify_jwt
from app.core.logger import get_logger

from app.query.clean_question import clean_question
from app.query.retriever import retrieve_chunks
from app.query.context_builder import build_context
from app.query.confidence import calculate_confidence
from app.query.llm_runner import get_rag_chain
from app.query.prompt_builder import build_chat_prompt

router = APIRouter(prefix="/query", tags=["Query"])
logger = get_logger()

rag_chain = get_rag_chain()


@router.post("/", response_model=QueryResponse)
def query_knowledge(
    req: QueryRequest,
    user=Depends(verify_jwt),
):
    start_time = time.time()
    user_id = user.get("sub", "unknown")

    logger.info(f"user={user_id} action=query start")

    # 1️⃣ Clean question
    question = clean_question(req.question)

    # 2️⃣ Retrieve docs + similarity scores
    retrieved = retrieve_chunks(question)

    # Guard: no relevant documents found
    if not retrieved:
        logger.warning(
            f"user={user_id} action=query no_relevant_docs"
        )
        return QueryResponse(
            answer="No relevant information found in the knowledge base.",
            confidence=0.0,
            sources=[]
        )

    # 3️⃣ Confidence calculation
    scores = [score for _, score in retrieved]
    confidence = calculate_confidence(scores)

    # 4️⃣ Build document context
    context = build_context(retrieved)

    # 5️⃣ Build conversational (ChatGPT-style) prompt
    prompt = build_chat_prompt(
        question=question,
        chat_history=req.chat_history,
        context=context,
    )

    # 6️⃣ LLM call (single prompt string)
    llm_response = rag_chain.invoke(prompt)

    # Normalize response
    answer = (
        llm_response.content
        if hasattr(llm_response, "content")
        else str(llm_response)
    )

    # 7️⃣ Extract sources
    sources = list({
        doc.metadata.get("source_file")
        for doc, _ in retrieved
        if doc.metadata.get("source_file")
    })

    duration_ms = int((time.time() - start_time) * 1000)

    logger.info(
        f"user={user_id} action=query success "
        f"confidence={confidence} duration_ms={duration_ms}"
    )

    return QueryResponse(
        answer=answer,
        confidence=confidence,
        sources=sources
    )
