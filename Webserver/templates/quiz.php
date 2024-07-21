<?php
    echo '<pre>';
    print_r($_POST);
    print_r($_SESSION);
    echo '</pre>';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>License Quiz</title>
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
        #time {
            float: right;
            color: #fff;
            font-size: 20px;
            margin-right: 20px;
        }
        form {
            background: #fff;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .question {
            padding: 20px;
            margin-bottom: 20px;
            border: 2px solid rgb(151, 153, 152);
            border-radius: 5px;
        }
        .question p {
            font-size: 18px;
        }
        .options {
            margin-top: 10px;
        }
        .options input {
            margin-right: 10px;
        }
        .image-box {
            float: right;
            width: 40%;
            margin-left: 20px;
        }
        .image-box img {
            max-width: 100%;
            height: auto;
        }
        .clear {
            clear: both;
        }
        button {
            display: inline-block;
            background: #333;
            color: #fff;
            padding: 10px 20px;
            font-size: 18px;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: #0779e4;
        }
    </style>
    <script>
        function startTimer(duration, display) {
            var timer = duration, minutes, seconds;
            setInterval(function () {
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);
                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;
                display.textContent = minutes + ":" + seconds;
                if (--timer < 0) {
                    timer = duration;
                    document.getElementById("quizForm").submit();
                }
            }, 1000);
        }
        window.onload = function () {
            var twentyMinutes = 60 * 20,
                display = document.querySelector('#time');
            startTimer(twentyMinutes, display);
        };
    </script>
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
