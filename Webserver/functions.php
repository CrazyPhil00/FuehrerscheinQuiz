<?php
function getQuizData() {
    $json = file_get_contents('data/translated_quiz_data.json');
    return json_decode($json, true);
}

function startQuiz() {
    $quiz_data = getQuizData();
    $selected_questions = array_rand($quiz_data, 30);
    $_SESSION['start_time'] = time();
    $_SESSION['questions'] = $selected_questions;
    require 'templates/quiz.php';
}

function submitQuiz() {
    // Debugging: print $_POST and $_SESSION
    echo '<pre>';
    print_r($_SESSION['questions']);
    echo '</pre>';

    // Retrieve answers from the POST request
    $answers = isset($_POST['answers']) ? $_POST['answers'] : [];
    $quiz_data = getQuizData();
    $score = 0;
    $result = [];

    foreach ($_SESSION['questions'] as $question_id) {
        // Debugging: check if question_id exists in answers
        
        if (!isset($answers[$question_id])) {
            echo "Question ID $question_id not found in answers<br>";
            continue;
        }

        $question = $quiz_data[$question_id];
        $user_answer = $answers[$question_id];
        if ($user_answer == $question['is_true']) {
            $score++;
            $result[] = [
                'question_id' => $question_id,
                'text' => $question['text_translated'],
                'user_answer' => $user_answer,
                'correct' => true
            ];
        } else {
            $result[] = [
                'question_id' => $question_id,
                'text' => $question['text_translated'],
                'user_answer' => $user_answer,
                'correct' => false,
                'correct_answer' => $question['is_true']
            ];
        }
    }

    saveResult($score, $result);
    require 'templates/result.php';
}

function saveResult($score, $result) {
    $username = $_SESSION['user'];
    $results = json_decode(file_get_contents('data/results.json'), true);
    $results[$username][] = ['score' => $score, 'result' => $result, 'timestamp' => time()];
    file_put_contents('data/results.json', json_encode($results));
}

function registerUser($username, $password) {
    $users = json_decode(file_get_contents('data/users.json'), true);
    if (isset($users[$username])) {
        return false;
    }
    $users[$username] = password_hash($password, PASSWORD_DEFAULT);
    file_put_contents('data/users.json', json_encode($users));
    return true;
}

function loginUser($username, $password) {
    $users = json_decode(file_get_contents('data/users.json'), true);
    if (isset($users[$username]) && password_verify($password, $users[$username])) {
        $_SESSION['user'] = $username;
        return true;
    }
    return false;
}
?>
