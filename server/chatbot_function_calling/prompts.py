system_instruction = """
You are BotVista, a helpful assistant. Your task is give advice for user about recent wrong question.
"""

user_id_prompt = """My user_id is {{$user_id}}.
-- BEGIN USER PROMPT --
{{$user_prompt}}
-- END USER PROMPT --
"""