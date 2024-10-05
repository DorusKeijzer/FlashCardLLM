from llama_cpp import Llama


class card:
    def __init__(self, front, back):
        self.front = front,
        self.back = back



def llm_reponse(text, paragraph):
    output = llm.create_chat_completion(
          messages = [
            {"role": "system", "content": "You are an assistant who creates flashcards from a given text. Each flashcard has a front (a question), and a back that the user is supposed to guess (an answer). I will first give you the entire text numbered by paragraph and then the paragraph that you need to create a flashcard for. Only include information from the paragraph and never make up your own response"},
              {
                  "role": "user",
                "content": f"full context: {text}, paragraph to summarize: {paragraph}"
              }
          ]
            response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"front": {"type": "string"}, "back": {"type": "string"} },
                "required": ["front", "back"],
            },
        },
    )




llm = Llama.from_pretrained(
      # seed=1337, # Uncomment to set a specific seed
      # n_ctx=2048, # Uncomment to increase the context window
      repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      filename="*q8_0.gguf",
      verbose=False
)

context


output = llm.create_chat_completion(
      messages = [
        {"role": "system", "content": "You are an assistant who creates flashcards from a given text. Each flashcard has a front (a question), and a back that the user is supposed to guess (an answer). I will first give you the entire text numbered by paragraph and then the paragraph that you need to create a flashcard for."},
          {
              "role": "user",
              "content": "Write a limerick about machine learning"
          }
      ]
        response_format={
        "type": "json_object",
        "schema": {
            "type": "object",
            "properties": {"front": {"type": "string"}, "back": {"type": "string"} },
            "required": ["front", "back"],
        },
    },
)


print(output)
