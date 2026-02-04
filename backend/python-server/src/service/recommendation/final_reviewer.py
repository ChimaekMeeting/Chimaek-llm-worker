from langchain_core.output_parsers import StrOutputParser

class FinalReviewer:
    def __init__(self, gpt_client):
        self.gpt_client = gpt_client
        self.parser = StrOutputParser()

    async def generate_review_message(self, context: dict) -> str:
        """
        수집된 정보를 요약하여 최종 확인 질문을 생성합니다.
        """
        is_circular = context.get("is_circular")
        origin = context.get("origin")
        destination = origin if is_circular else context.get("destination")

        review_message = await self.gpt_client.get_response(
            prompt_name="final_review",
            input_data={
                "is_circular": "순환" if is_circular else "편도",
                "origin": origin,
                "destination": destination,
                "purpose": context.get("purpose")
            },
            output_parser=self.parser
        )

        return review_message