import json
import re
from django.conf import settings
from groq import Groq


def generate_tags_for_blog(title, content):
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return only a JSON array of blog tags."},
                {
                    "role": "user",
                    "content": f"""
Generate 5 tags for this blog.

Rules:
- Tags must match the blog topic.
- Do not copy any example tags.
- Return only a JSON array of lowercase strings.
- No explanation.

Title: {title}
Content: {content}
""",
                },
            ],
            temperature=0.3,
        )

        result = response.choices[0].message.content

        print("AI RAW RESULT:", result)

        if not result:
            return []

        match = re.search(r"\[.*\]", result, re.DOTALL)

        if not match:
            return []

        tags = json.loads(match.group())

        if isinstance(tags, list):
            return tags

        return []

    except Exception as e:
        print("TAG GENERATION ERROR:", e)
        return []
