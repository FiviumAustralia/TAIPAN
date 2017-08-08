function goBack() {
    window.history.back();
}

function confirm_cancellation() {
    if (confirm("Are you sure you want to cancel?")) {
        goBack();
    } else {
        return false;
    }
}

// Script to open and close sidebar
function open_sidebar() {
    document.getElementById("sidebar-left").style.display = "block";
}

function close_sidebar() {
    document.getElementById("sidebar-left").style.display = "none";
}