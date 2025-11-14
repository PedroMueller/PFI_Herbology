$(document).ready(function () {

    var targetUl = $('#myList');
    var items = ['Item A', 'Item B', 'Item C'];

    http://localhost:5000/data

    $.get("http://127.0.0.1:5000/data",
        function (data) {
            var items = data
            console.log(items)
            $.each(items, function (index, value) {
                targetUl.append('<li>' + value + '</li>');
            });
        }
    )

})