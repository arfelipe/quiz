import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_add_multiple_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    assert len(question.choices) == 2
    assert choice1.id != choice2.id

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    question.remove_choice_by_id(choice1.id)
    assert len(question.choices) == 0

def test_remove_non_existent_choice():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    question.set_correct_choices([choice1.id])
    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', is_correct=True)
    choice2 = question.add_choice('b')
    correct_selections = question.correct_selected_choices([choice1.id, choice2.id])
    assert len(correct_selections) == 1
    assert correct_selections[0] == choice1.id

def test_correct_selected_choices_with_invalid_selection_count():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id])

def test_default_max_selections():
    question = Question(title='q1')
    assert question.max_selections == 1

def test_correct_selected_choices_with_no_correct_selections():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    correct_selections = question.correct_selected_choices([choice1.id, choice2.id])
    assert len(correct_selections) == 0

@pytest.fixture
def question_with_choices():
    question = Question(title='New fixture question', max_selections=2)
    question.add_choice('Correct answer', is_correct=True)
    question.add_choice('Incorrect answer')
    return question

def test_question_has_choices(question_with_choices):
    assert len(question_with_choices.choices) == 2

def test_check_correct_choice(question_with_choices):
    correct_choices_ids = [choice.id for choice in question_with_choices.choices if choice.is_correct]
    selected_ids = question_with_choices.correct_selected_choices([correct_choices_ids[0]])
    assert len(selected_ids) == 1
    assert selected_ids[0] == correct_choices_ids[0]