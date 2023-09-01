var coeffDefaut = "";
var reductionDefaut = "";

function defaultCoeff(input) {
    coeffDefaut = input.value;
}

function defaultDiscount(input) {
    reductionDefaut = input.value;
}

$(document).ready(function() {
    $(document).on("change", "select[name='Article']", function() {
        updateTotalPrice(); // Mettez à jour le prix total
    });
    $(document).on("change", "input[name='nombre[]'], input[name='coeff[]'], input[name='reduction[]']", function() {
        updateTotalPrice(); // Mettez à jour le prix total
    });
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

    $("#generateButton").on("click", function() {
        return validateForm();
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

    var coeffValue = coeffDefaut !== "" ? coeffDefaut : "";
    var reductionValue = reductionDefaut !== "" ? reductionDefaut : "";

    var articleSelect = document.getElementById("Article").cloneNode(true);
    articleSelect.removeAttribute("hidden");

    articleCell.appendChild(articleSelect);

    nombreCell.innerHTML = '<input type="number" name="nombre[]" value="">';
    coeffCell.innerHTML = '<input type="number" name="coeff[]" value="' + coeffValue + '" onchange="defaultCoeff(this)">';
    reductionCell.innerHTML = '<input type="number" name="reduction[]" value="' + reductionValue + '" onchange="defaultDiscount(this)">';
    actionsCell.innerHTML = '<button type="button" onclick="supprimerLigne(this)">x</button>';
}

function supprimerLigne(button) {
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

function updateTotalPrice() {
    var totalPrice = 0;

    $("#tableInputs tr").each(function() {
        var articleSelect = $(this).find("select[name='Article']");
        var selectedOption = articleSelect.find("option:selected");

        var price = parseFloat(selectedOption.attr("data-price")) || 0;

        var nombreValue = parseFloat($(this).find("input[name='nombre[]']").val()) || 0;
        var coeffValue = parseFloat($(this).find("input[name='coeff[]']").val()) || 0;
        var reductionValue = parseFloat($(this).find("input[name='reduction[]']").val()) || 0;


        var totalLinePrice = price * coeffValue * nombreValue * (1 - reductionValue / 100);
        totalPrice += totalLinePrice;
    });

    $("#totalPrice").text("Total Price: " + totalPrice.toFixed(2) + "€");
    $("#totalTVA").text("Total TVA: " + (totalPrice*1.2).toFixed(2) + "€");
}

function validateForm() {
    var tableRows = document.querySelectorAll("#tableInputs tr");
    var isValid = true;
    var isValid2 = true;
    var count = 0;

    for (var i = 1; i < tableRows.length; i++) {
        var row = tableRows[i];
        var articleSelect = row.querySelector("select[name='Article']");
        var selectedValue = articleSelect.value;
        var selectedValue2 = row.querySelector("input[name='nombre[]']").value;

        if (selectedValue === "") {
            isValid = false;
            count += 1;
        }

        if (selectedValue2 === "") {
            isValid2 = false;
        }
    }

    if (count > 0) {
        isValid = false;
    }

    if (!isValid) {
        alert("You cannot have neither no article nor any null articles.");
        return false;
    }

    if (!isValid2) {
        alert("You cannot have an empty number field.");
        return false;
    }

    return true;
}