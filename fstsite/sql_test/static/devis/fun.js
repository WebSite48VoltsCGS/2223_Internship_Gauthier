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
                            }
                            else{
                                nameSpan.textContent = `${article.name} `;
                            }

                            const input = document.createElement('input');
                            input.type = 'number';
                            input.min = 0;
                            input.max = 100;
                            input.setAttribute('placeholder', 'Discount-%');
                            input.name = `discount_${article.id}`;

                            articleDiv.appendChild(nameSpan);
                            articleDiv.appendChild(input);

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