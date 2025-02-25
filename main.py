from dotenv import load_dotenv


load_dotenv()

from graph.graph import app

question = "Podrías resumirme todo el libro?"


if __name__ == "__main__":

    print("Running the app")
    print(app.invoke(input={"question": question}))








