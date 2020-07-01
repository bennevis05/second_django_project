// Создаем объект Intl.NumberFormat для удобного форматирования чисел
let formatter = new Intl.NumberFormat('ru', {minimumFractionDigits: 2});

currentElements = document.getElementsByClassName('formatted-price');
for(let i = 0; i < currentElements.length; i++) {
    price = currentElements[i].innerText.split(',')[0];
    currentElements[i].innerText = formatter.format(price) + ' руб.';
}
