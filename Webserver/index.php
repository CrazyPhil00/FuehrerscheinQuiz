<?php
session_start();
require 'functions.php';

$page = isset($_GET['page']) ? $_GET['page'] : 'home';

if ($page == 'home') {
    require 'templates/home.php';
} elseif ($page == 'start_quiz') {
    if (!isset($_SESSION['user'])) {
        header('Location: index.php?page=login');
        exit();
    }
    startQuiz();
} elseif ($page == 'submit_quiz') {
    submitQuiz();
} elseif ($page == 'login') {
    require 'templates/login.php';
} elseif ($page == 'logout') {
    session_destroy();
    header('Location: index.php?page=home');
}
?>
