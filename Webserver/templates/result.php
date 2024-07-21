<?php

if (!isset($_SESSION['user'])) {
    header('Location: login.php');
    exit();
}

$results_file = 'data/results.json';

if (!file_exists($results_file)) {
    echo "No results found.";
    exit();
}

$results = json_decode(file_get_contents($results_file), true);
$username = $_SESSION['user'];

if (!isset($results[$username])) {
    echo "No results found for user.";
    exit();
}

$user_results = $results[$username];
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
        }
        header {
            background: #333;
            color: #fff;
            padding-top: 30px;
            min-height: 70px;
            border-bottom: #0779e4 3px solid;
        }
        header a {
            color: #fff;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 16px;
        }
        .results {
            background: #fff;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .result-item {
            border: 2px solid rgb(151, 153, 152);
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .result-item p {
            font-size: 18px;
        }
        .clear {
            clear: both;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>License Quiz</h1>
            <div id="time">20:00</div>
        </div>
    </header>
    <div class="container">
        <form id="quizForm" action="index.php?page=submit_quiz" method="POST">
            <?php foreach ($_SESSION['questions'] as $question_id): ?>
                <?php $question = $quiz_data[$question_id]; ?>
                <div class="question">
                    <div class="image-box">
                        <?php if ($question['has_image']): ?>
                            <img src="static/<?php echo $question['has_image']; ?>" alt="Question Image">
                        <?php endif; ?>
                    </div>
                    <p><?php echo $question['id']; ?>. <?php echo $question['text_translated']; ?></p>
                    <div class="options">
                        <input type="radio" name="answers[<?php echo $question['id']; ?>]" value="VERO" required> Richtig
                        <input type="radio" name="answers[<?php echo $question['id']; ?>]" value="FALSO" required> Falsch
                    </div>
                    <div class="clear"></div>
                </div>
            <?php endforeach; ?>
            <button type="submit">Submit Quiz</button>
        </form>
    </div>
</body>
</html>