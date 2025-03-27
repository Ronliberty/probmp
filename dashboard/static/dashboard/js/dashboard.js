   $(document).ready(function() {
  // Target all <a> elements inside <li> and remove text-decoration
  $('li a').css('text-decoration', 'none');
});

$(document).ready(function () {
    $(".dropdown-header").on("click", function () {
        $(this).toggleClass("active"); // Toggle active class for rotation
        $(this).next(".dropdown-content").slideToggle(300); // Toggle visibility
    });
});


const toggle = document.getElementById('toggleDark');
const body = document.querySelector('body');
const allElements = document.querySelectorAll('*');
const specificElements = [
    document.querySelector('.sidebar'),
    document.querySelector('.header'),
    document.querySelector('.footerbar'),
    document.querySelector('.container'),
];

toggle.addEventListener('click', function () {
    // Toggle dark mode icon
    this.classList.toggle('bi-moon');
    this.classList.toggle('bi-brightness-high-fill');

    const isLightMode = this.classList.contains('bi-brightness-high-fill');

    // Define color scheme
    const lightBackground = '#f1f1f1'; // Light grey background for light mode
    const darkBackground = '#121212'; // Deep dark background for dark mode
    const lightText = '#000'; // Black text for light mode
    const darkText = '#E0E0E0'; // Light grey text for dark mode
    const linkColorLight = '#1E88E5'; // Light blue for links in light mode
    const linkColorDark = '#BB86FC'; // Purple for links in dark mode
    const elementBackgroundLight = '#fff'; // White background for specific elements in light mode
    const elementBackgroundDark = '#1E1E1E'; // Slightly lighter dark grey for specific elements in dark mode
    const buttonBackgroundLight = '#6200EE'; // Purple for buttons in light mode
    const buttonBackgroundDark = '#3700B3'; // Dark purple for buttons in dark mode

    // Set global styles based on the current mode
    const backgroundColor = isLightMode ? lightBackground : darkBackground;
    const textColor = isLightMode ? lightText : darkText;
    const linkColor = isLightMode ? linkColorLight : linkColorDark;
    const buttonBackground = isLightMode ? buttonBackgroundLight : buttonBackgroundDark;
    const elementBackground = isLightMode ? elementBackgroundLight : elementBackgroundDark;

    // Apply styles to the body
    body.style.backgroundColor = backgroundColor;
    body.style.color = textColor;

    // Apply styles to all elements
    allElements.forEach(element => {
        element.style.transition = '0.5s';
        if (element.tagName === 'A' || element.tagName === 'LI') {
            element.style.color = linkColor;
            element.style.textDecoration = 'none';
        } else {
            element.style.backgroundColor = backgroundColor;
            element.style.color = textColor;
        }
    });

    // Apply specific styles to key elements
    specificElements.forEach(element => {
        if (element) {
            element.style.backgroundColor = elementBackground;
        }
    });

    // Apply button colors (if buttons exist)
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.style.backgroundColor = buttonBackground;
        button.style.color = textColor;
    });

    // Smooth transitions for all elements
    body.style.transition = '0.5s';
});


  </script>