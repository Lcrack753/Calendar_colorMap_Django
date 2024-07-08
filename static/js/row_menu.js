const displayViewsbyMenu = function (row_menu_id) {
    const menu = document.getElementById(row_menu_id); // Get the menu by ID
    const btns = menu.getElementsByClassName('small-menu-item'); // Get all menu items

    const views = document.getElementsByClassName('view'); // Get all elements with class 'view'

    Array.from(btns).forEach(function (btn) {
        btn.addEventListener('click', function () {
            let data = btn.getAttribute('data');

            // Remove 'active' class from all buttons
            Array.from(btns).forEach(function (b) {
                b.classList.remove('active');
            });

            // Add 'active' class to the clicked button
            btn.classList.add('active');

            // Show/hide views based on the clicked menu item
            Array.from(views).forEach(function (element) {
                if (element.id === data) {
                    element.classList.add('active');
                } else {
                    element.classList.remove('active');
                }
            });
        });
    });
}

