<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST['login'])) {
            if (loginUser($_POST['username'], $_POST['password'])) {
                header('Location: index.php?page=home');
            } else {
                echo "<p>Invalid credentials!</p>";
            }
        } elseif (isset($_POST['register'])) {
            if (registerUser($_POST['username'], $_POST['password'])) {
                echo "<p>Registration successful! Please log in.</p>";
            } else {
                echo "<p>Username already exists!</p>";
            }
        }
    }
    ?>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit" name="login">Login</button>
        <button type="submit" name="register">Register</button>
    </form>
    <a href="index.php?page=home">Go to Home</a>
</body>
</html>
