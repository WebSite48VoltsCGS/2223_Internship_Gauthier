$(document).ready(function() {
    $('#Commande').on('input', function() {
        var input = $(this).val().toLowerCase();
        $('#Commande option').each(function() {
            if ($(this).text().toLowerCase().indexOf(input) === -1) {
                $(this).prop('hidden', true);
            } else {
                $(this).prop('hidden', false);
            }
        });
    });


    $('#Article').on('input', function() {
        var input = $(this).val().toLowerCase();
        $('#Article option').each(function() {
            if ($(this).text().toLowerCase().indexOf(input) === -1) {
                $(this).prop('hidden', true);
            } else {
                $(this).prop('hidden', false);
            }
        });
    });
});


function loadArticles() {
    const articlesContainer = document.getElementById('articles-list');
    const selectedBillingId = document.getElementById('Commande').value;
    articlesContainer.innerHTML = '';

    $.ajax({
        url: '/devis/',
        type: 'GET',
        data: {billing_id: selectedBillingId},
        success: function(response) {
            const lines = response.lines;
            if (lines) {
                for (const line of lines) {
                    var table = document.getElementById("tableInputs");
                    var newRow = table.insertRow();

                    var articleCell = newRow.insertCell(0);
                    var nombreCell = newRow.insertCell(1);
                    var coeffCell = newRow.insertCell(2);
                    var reductionCell = newRow.insertCell(3);
                    var actionsCell = newRow.insertCell(4);

                    var numberValue = line.number;
                    var coeffValue = line.coeff;
                    var reductionValue = line.discount;

                    var articleSelect = document.getElementById("Article").cloneNode(true);
                    articleSelect.removeAttribute("hidden");
                    var defaultValue = line.article ;
                    articleSelect.value = defaultValue;

                    articleCell.appendChild(articleSelect);

                    nombreCell.innerHTML = '<input type="number" name="nombre[]" value="' +numberValue+ '">';
                    coeffCell.innerHTML = '<input type="number" name="coeff[]" value="' + coeffValue+ '">';
                    reductionCell.innerHTML = '<input type="number" name="reduction[]" value="' + reductionValue+ '">';
                    actionsCell.innerHTML = '<button type="button" onclick="supprimerLigne(this)">x</button>';
                }

            }
        }
    })
}

function updateHiddenField() {
    var selectedValue = document.getElementById("Commande").value;
    document.getElementById("selected_value").value = selectedValue;
}

function ajouterLigne() {
    var table = document.getElementById("tableInputs");
    var newRow = table.insertRow();

    var articleCell = newRow.insertCell(0);
    var nombreCell = newRow.insertCell(1);
    var coeffCell = newRow.insertCell(2);
    var reductionCell = newRow.insertCell(3);
    var actionsCell = newRow.insertCell(4);

    var articleSelect = document.getElementById("Article").cloneNode(true);
    articleSelect.removeAttribute("hidden");

    articleCell.appendChild(articleSelect);

    nombreCell.innerHTML = '<input type="number" name="nombre[]" value="">';
    coeffCell.innerHTML = '<input type="number" name="coeff[]">';
    reductionCell.innerHTML = '<input type="number" name="reduction[]">';
    actionsCell.innerHTML = '<button type="button" onclick="supprimerLigne(this)">x</button>';
}

function supprimerLigne(button) {
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}