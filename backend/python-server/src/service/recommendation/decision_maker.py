from langchain_core.output_parsers import StrOutputParser
import re

class DecisionMaker:
    def __init__(self, gpt_client):
        self.gpt_client = gpt_client
        self.parser = StrOutputParser()

    async def is_user_confirmed(self, user_prompt: str) -> bool:
        """
        제안된 산책 조건에 대한 동의 여부를 반환합니다.

        Returns:
            - 동의 -> True
            - 거절/수정 요청 -> False
        """
        response = await self.gpt_client.get_response(
            prompt_name="decision",
            input_data={"user_prompt": user_prompt},
            output_parser=self.parser
        )

        # 숫자만 필터링
        match = re.search(r"\d+", response)

        if match:
            digit = match.group()
            return digit == "1"

        return False