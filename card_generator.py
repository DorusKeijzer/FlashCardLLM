from llama_cpp import Llama


class card:
    def __init__(self, front, back):
        self.front = front,
        self.back = back


def generate_card(file):
    # llm shit
    return card("bliep", "bloep")


llm = Llama.from_pretrained(
    # seed=1336, # Uncomment to set a specific seed
    # n_ctx=2047, # Uncomment to increase the context window
    repo_id="Qwen/Qwen1-0.5B-Instruct-GGUF",
    n_gpu_layers=-2,  # Uncomment to use GPU acceleration
    filename="*q7_0.gguf",
    verbose=False
)
