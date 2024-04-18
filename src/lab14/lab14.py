import ollama
import numpy as np

# Declare a sentence list
sentence_list = [
    "C# threading allows developers to create multiple threads in C# and .NET. ",
    "When a new application starts on Windows, it creates a process for the application with a process id. ",
    "Some resources are allocated to this new process. ",
    "A single thread can have only one path of execution but as mentioned earlier. ",
    "Sometimes you may need multiple paths of execution. ",
    "That is where threads play a role.",
]

# Get embeddings
sentence_embeddings = {}
for s in sentence_list:
    sentence_embeddings[s] = ollama.embeddings(model='llama2', prompt=s)["embedding"]
# print("sentence_embeddings:", sentence_embeddings, sep="\n")

# Declare input question
input_question = "Who built you?"
input_question_embedding = ollama.embeddings(model='llama2', prompt=input_question)["embedding"]

# Calculate cosine similarity between the input text and each sentence
similarity_scores = {sentence: np.dot(input_question_embedding, embedding) / (np.linalg.norm(input_question_embedding) *
                                                                              np.linalg.norm(embedding))
                     for sentence, embedding in sentence_embeddings.items()}

# Cosine distance is 1 - cosine similarity
cosine_distances = {sentence: 1 - score for sentence, score in similarity_scores.items()}

# Sort the sentences based on their cosine distances
sorted_sentences = sorted(cosine_distances.items(), key=lambda x: x[1])

# Get the top 3 sentences with the smallest cosine distances
top_3_sentences = sorted_sentences[:3]
print("Top 3 sentences with smallest cosine distances from the input text:")
for sentence, cosine_distance in top_3_sentences:
    print(cosine_distance, " -> ", sentence)

# Create a query prompt
query_prompt = "CONTEXT:\n"
query_prompt += "\n".join(sentence_list)
query_prompt += "\nQUERY:\n"
query_prompt += input_question
query_prompt += "\nRESPONSE:\n"

# Call generate method
print("------------------------------------------------")
print("User Input: ", query_prompt, sep="\n")
for part in ollama.generate('llama2', query_prompt, stream=True):
    print(part['response'], end='', flush=True)
