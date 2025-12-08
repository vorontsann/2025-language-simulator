import FreeSimpleGUI as sg

from src.data_manager.csv_data_manager import CSVDataManager
from src.data_manager.sqlite_user_manager import SQLiteUserManager
from src.models.language import Language
from src.models.topic import Topic
from src.quiz.quiz_session import QuizSession


# ---------- User windows ----------

def create_user_window(user_manager: SQLiteUserManager) -> int | None:
    """Create or select a user."""
    layout = [
        [sg.Text('Enter username')],
        [sg.Input(key='USERNAME')],
        [sg.Button('Create'), sg.Button('Cancel')],
    ]

    window = sg.Window('Create User', layout)
    event, values = window.read()
    window.close()

    if event != 'Create':
        return None

    username = values.get('USERNAME')
    if not username:
        sg.popup('Username cannot be empty')
        return None

    user = user_manager.get_user_by_name(username)
    if user is None:
        user_id = user_manager.create_user(username)
        sg.popup(f'User "{username}" created')
        return user_id

    sg.popup(f'User "{username}" selected')
    return user[0]


def show_progress_window(user_manager: SQLiteUserManager, user_id: int):
    """Show progress of the user from SQLite."""
    stats = user_manager.get_user_stats(user_id)
    if not stats:
        sg.popup('No user statistics found')
        return

    total, correct = stats
    accuracy = correct / total if total > 0 else 0

    layout = [
        [sg.Text(f'User ID: {user_id}')],
        [sg.Text(f'Total answers: {total}')],
        [sg.Text(f'Correct answers: {correct}')],
        [sg.Text(f'Accuracy: {accuracy:.2%}')],
        [sg.Button('Close')],
    ]

    sg.Window('User Progress', layout).read(close=True)


# ---------- Quiz logic ----------

def run_quiz_session(session: QuizSession):
    """Run the quiz loop."""
    while True:
        word = session.next_item()
        if not word:
            break

        layout = [
            [sg.Text(f'Translate:', font=('Helvetica', 10))],
            [sg.Text(word.term, font=('Helvetica', 16))],
            [sg.Input(key='ANSWER')],
            [sg.Button('Submit'), sg.Button('Hint')],
        ]

        window = sg.Window('Quiz', layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Submit'):
                answer = values.get('ANSWER', '')
                is_correct = session.check_answer(answer)

                if is_correct:
                    sg.popup('✅ Correct!')
                else:
                    sg.popup(
                        '❌ Wrong!',
                        f'Correct answer: {session.get_correct_answer()}'
                    )
                break

            if event == 'Hint':
                sg.popup('Hint', session.show_hint())

        window.close()

    results = session.get_results()

    sg.popup(
        'Session finished',
        f'Correct: {results["correct"]}',
        f'Wrong: {results["wrong"]}',
        f'Accuracy: {results["accuracy"]:.2%}',
    )


def start_quiz_window(
    user_id: int,
    data_manager: CSVDataManager,
    user_manager: SQLiteUserManager,
):
    """Select language, topic and start quiz session."""
    layout = [
        [sg.Text('Select language')],
        [sg.Combo([lang.name for lang in Language], key='LANGUAGE')],
        [sg.Text('Select topic')],
        [sg.Combo([topic.value for topic in Topic], key='TOPIC')],
        [sg.Button('Start'), sg.Button('Cancel')],
    ]

    window = sg.Window('Quiz setup', layout)
    event, values = window.read()
    window.close()

    if event != 'Start':
        return

    if not values.get('LANGUAGE') or not values.get('TOPIC'):
        sg.popup('Please select both language and topic')
        return

    language = Language[values['LANGUAGE']]
    topic = Topic(values['TOPIC'])

    session = QuizSession(
        user_id=user_id,
        language=language,
        topic=topic,
        data_manager=data_manager,
        user_manager=user_manager,
    )

    run_quiz_session(session)


# ---------- Main app ----------

def run_app():
    """Main application window."""
    sg.theme('DarkBlue3')

    user_manager = SQLiteUserManager()
    data_manager = CSVDataManager()

    layout = [
        [sg.Text('Language Simulator', font=('Helvetica', 16))],
        [sg.Button('Create user'), sg.Button('View progress')],
        [sg.Button('Start quiz')],
        [sg.Button('Exit')],
    ]

    window = sg.Window('Language Trainer', layout)
    current_user_id: int | None = None

    while True:
        event, _ = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        if event == 'Create user':
            current_user_id = create_user_window(user_manager)

        elif event == 'View progress':
            if current_user_id is None:
                sg.popup('Create or select a user first')
            else:
                show_progress_window(user_manager, current_user_id)

        elif event == 'Start quiz':
            if current_user_id is None:
                sg.popup('Create or select a user first')
            else:
                start_quiz_window(current_user_id, data_manager, user_manager)

    window.close()
