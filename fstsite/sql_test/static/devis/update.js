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
    const selectedBillingId = document.getElementById('Commande').value;

    $.ajax({
        url: '/devis/update/',
        type: 'GET',
        data: {billing_id: selectedBillingId},
        success: function(response) {
            const lines = response.lines;
            const command = response.commande;
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
            if (command){
                var name = document.getElementById("nomPrestation") ;
                var place = document.getElementById("lieuPrestation") ;
                var dateS = document.getElementById("debPrestation");
                var dateE = document.getElementById("finPrestation") ;
                var dep = document.getElementById("Deposit") ;

                dateStart = command.start.slice(0, -1);
                dateEnd = command.end.slice(0, -1);

                name.value = command.desc;
                place.value = command.place;
                dateS.value = dateStart;
                dateE.value = dateEnd;
                dep.value = command.dep;
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