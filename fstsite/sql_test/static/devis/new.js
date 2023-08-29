$(document).ready(function() {
    $('#Client').on('input', function() {
        var input = $(this).val().toLowerCase();
        $('#Client option').each(function() {
            if ($(this).text().toLowerCase().indexOf(input) === -1) {
                $(this).prop('hidden', true);
            } else {
                $(this).prop('hidden', false);
            }
        });
    });
});

function ajouterLigne() {
    var table = document.getElementById("tableInputs");
    var newRow = table.insertRow();

    var articleCell = newRow.insertCell(0);
    var nombreCell = newRow.insertCell(1);
    var coeffCell = newRow.insertCell(2);
    var reductionCell = newRow.insertCell(3);
    var actionsCell = newRow.insertCell(4);

    articleCell.innerHTML = '<input type="text" name="article[]">';
    nombreCell.innerHTML = '<input type="number" name="nombre[]">';
    coeffCell.innerHTML = '<input type="number" name="coeff[]">';
    reductionCell.innerHTML = '<input type="number" name="reduction[]">';
    actionsCell.innerHTML = '<button onclick="supprimerLigne(this)">x</button>';
    console.log("je suis passé ici") ;
}

function supprimerLigne(button) {
    console.log("je suis passé là") ;
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}