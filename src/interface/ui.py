import FreeSimpleGUI as sg # type: ignore

from src.models.language import Language
from src.models.topic import Topic
from src.quiz.quiz_session import QuizSession
from src.data_manager.csv_data_manager import MockDataManager
from src.data_manager.progress_manager import ProgressManager


def create_user_window() -> str | None:
    layout = [
        [sg.Text("Enter user ID")],
        [sg.Input(key="USER_ID")],
        [sg.Button("Create"), sg.Button("Cancel")]
    ]

    window = sg.Window("Create User", layout)
    event, values = window.read()
    window.close()

    if event == "Create" and values["USER_ID"]:
        return values["USER_ID"]

    return None


def show_progress_window(
    progress_manager: ProgressManager,
    user_id: str
):
    progress = progress_manager.get_user_progress(user_id)

    layout = [
        [sg.Text(f"User: {user_id}")],
        [sg.Text(f"Correct answers: {progress.correct}")],
        [sg.Text(f"Wrong answers: {progress.wrong}")],
        [sg.Text(f"Accuracy: {progress.accuracy:.2%}")],
        [sg.Button("Close")]
    ]

    sg.Window("User Progress", layout).read(close=True)


def run_quiz_session(session: QuizSession):
    while True:
        word = session.next_item()
        if not word:
            break

        layout = [
            [sg.Text(f"Translate: {word.term}", font=("Helvetica", 14))],
            [sg.Input(key="ANSWER")],
            [sg.Button("Submit"), sg.Button("Hint")]
        ]

        window = sg.Window("Quiz", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Submit"):
                answer = values.get("ANSWER", "")
                is_correct = session.check_answer(answer)

                if is_correct:
                    sg.popup("Correct!")
                else:
                    sg.popup(
                        "Wrong!",
                        f"Correct answer: {session.get_correct_answer()}"
                    )
                break

            if event == "Hint":
                sg.popup("Hint", session.show_hint())

        window.close()

    results = session.get_results()
    sg.popup(
        "Session finished",
        f"Correct: {results['correct']}",
        f"Wrong: {results['wrong']}",
        f"Accuracy: {results['accuracy']:.2%}"
    )


def start_quiz_window(
    user_id: str,
    data_manager: MockDataManager,
    progress_manager: ProgressManager
):
    layout = [
        [sg.Text("Select language")],
        [sg.Combo(
            [lang.name for lang in Language],
            key="LANGUAGE"
        )],
        [sg.Text("Select topic")],
        [sg.Combo(
            [topic.value for topic in Topic],
            key="TOPIC"
        )],
        [sg.Button("Start"), sg.Button("Cancel")]
    ]

    window = sg.Window("Quiz setup", layout)
    event, values = window.read()
    window.close()

    if event != "Start":
        return

    language = Language[values["LANGUAGE"]]
    topic = Topic(values["TOPIC"])

    session = QuizSession(
        user_id=user_id,
        language=language,
        topic=topic,
        data_manager=data_manager,
        progress_manager=progress_manager
    )

    run_quiz_session(session)


def run_app():
    sg.theme("DarkBlue3")

    progress_manager = ProgressManager()
    data_manager = MockDataManager
    layout = [
        [sg.Text("Language Simulator", font=("Helvetica", 16))],
        [sg.Button("Create user"), sg.Button("View progress")],
        [sg.Button("Start quiz")],
        [sg.Button("Exit")]
    ]

    window = sg.Window("Language Trainer", layout)

    current_user_id = None

    while True:
        event, _ = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "Create user":
            current_user_id = create_user_window()

        elif event == "View progress":
            if not current_user_id:
                sg.popup("Create or select a user first")
            else:
                show_progress_window(progress_manager, current_user_id)

        elif event == "Start quiz":
            if not current_user_id:
                sg.popup("Create or select a user first")
            else:
                start_quiz_window(
                    current_user_id,
                    data_manager,
                    progress_manager
                )

    window.close()
