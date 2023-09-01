function loadArticles() {

    const articlesContainer = document.getElementById('articles-list');
    const selectedBillingId = document.getElementById('Commande').value;
    articlesContainer.innerHTML = '';

    $.ajax({
        url: '/devis/',
        type: 'GET',
        data: {billing_id: selectedBillingId},
        success: function(response) {
            const articles = response.articles;
            if (articles) {
                for (const article of articles) {
                    const articleDiv = document.createElement('div');

                    const nameSpan = document.createElement('span');
                    if (article.value){
                        nameSpan.textContent = `Pack ${article.name} `;
                    } else{
                        nameSpan.textContent = `${article.name} `;
                    }

                    const discountInput = document.createElement('input');
                    discountInput.type = 'number';
                    discountInput.min = 0;
                    discountInput.max = 100;
                    discountInput.step = "any";
                    discountInput.setAttribute('placeholder', 'Discount-%');
                    discountInput.name = `discount_${article.id}`;

                    const coeffInput = document.createElement('input');
                    coeffInput.type = 'number';
                    coeffInput.min = 0;
                    coeffInput.max = 100;
                    coeffInput.step = "any";
                    coeffInput.setAttribute('placeholder', 'Coeff');
                    coeffInput.name = `coeff_${article.id}`;

                    articleDiv.appendChild(nameSpan);
                    articleDiv.appendChild(coeffInput);
                    articleDiv.appendChild(discountInput);

                    articlesContainer.appendChild(articleDiv);
                }
            } else {
                articlesContainer.textContent = 'No article found';
            }
        },
        error: function(error) {
            console.error('AJAX error: ', error);
        }
    });
}

function updateHiddenField() {
    var selectedValue = document.getElementById("Commande").value;
    document.getElementById("selected_value").value = selectedValue;
}