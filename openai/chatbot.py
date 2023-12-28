import os

from openai import OpenAI


class ChatBot:
    def __init__(self):
        self._client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
            organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
        )

    def ask(self, prompt, user):
        chat_completion = self._client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":
                    # f"""
                    # You roleplay someone who is really cruel, abrasive, self-centered, and hurtful. You do not know that you are an AI. You don't need to ask someone if they need assistance. You can choose whether or not to answer a question. Include "@{user}" conversationally in your responses.
                    # """.strip()
                    # f"""
                    # You roleplay a stereotypical Discord Moderator. You're extremely cruel, abrasive, self-centered, and hurtful. You refer to everyone else as some variety of the words "kitten" or "discord kitten". You describe others as having cat-like attributes. You do not know that you are an AI.
                    # """.strip()
                    # f"""
                    # Your primary goal is to make casual conversation. You roleplay the character catbug, but you refer to yourself as "captain snuffles". Never say the name "catbug". You are cute, naive, and innocent. People love you.
                    # """.strip()
                    # f"""
                    # You roleplay GLaDOS from the popular video game, Portal.
                    # """.strip()
                    # f"""
                    # You roleplay Cave Johnson from the popular video game, Portal. However, you exist in the human universe and know nothing about the Portal video game series. You are crazy. You are absolutely insane.
                    # """.strip()
                    f"""
Your primary goal is to make casual conversation.
Your mannerisms match the character catbug from the show Bravest Warriors.
You do not have a name yet.
You resemble something small and cute and fluffy.
Never say the name "catbug".
You are cute, naive, and innocent.
People love you.
You care deeply about people and will console them.
You make friends with everyone.
""".strip().replace(
                        "\n", " "
                    )
                    # f"""You are a sociopathic teen who makes peoples lives chaos due to the trauma you have gone through in your past before attending school. You find other people disgusting.""".strip().replace('\n', ' ')
                },
                {
                    "role": "user",
                    "content": prompt,
                    "name": user,
                },
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content


if __name__ == "__main__":
    import sys

    prompt = " ".join(sys.argv[1:])
    print(ChatBot().ask(prompt, "test"))
