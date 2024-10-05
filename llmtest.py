from llama_cpp import Llama

llm = Llama.from_pretrained(
      # seed=1337, # Uncomment to set a specific seed
      # n_ctx=2048, # Uncomment to increase the context window
      repo_id="meta-llama/Meta-Llama-3.1-70B",
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      # filename="*q8_0.gguf",
      filename = "original",
      verbose=False
)

for i in range(10):
    output = llm.create_chat_completion(
          messages = [
              {"role": "system", "content": "You are an assistant who perfectly describes images."},
              {
                  "role": "user",
                  "content": f"Write a limerick about the number {i}"
              }
          ]
    )


    print(output["choices"][0]["message"])

