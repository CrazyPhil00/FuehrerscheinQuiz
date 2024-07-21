<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>License Quiz</title>
</head>
<body>
    <h1>Welcome to the License Quiz</h1>
    <p>You have 20 minutes to complete 30 questions.</p>
    <?php if (isset($_SESSION['user'])): ?>
        <a href="index.php?page=start_quiz">Start Quiz</a> | <a href="index.php?page=logout">Logout</a>
    <?php else: ?>
        <a href="index.php?page=login">Login</a>
    <?php endif; ?>
</body>
</html>
