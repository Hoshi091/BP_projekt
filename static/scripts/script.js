
var labelTexts = {
    'en': {
        'language_picker_label': 'Select the language of your page and app:',
        'url_label': 'Enter URL:',
        'get_links_label': 'Get links instead of text',
        'get_full_links_label': 'Get only http/https links',
        'keyword_input_label': '[Optional]Enter searched Keyword:',
        'get_dynamic_content_label': 'Page is dynamic',
        'pagination_scrape_label': 'Scrape with pagination',
        'pagination_count_label': 'Enter number of pages to scrape',
        'clean_stopwords_label': 'Clean stopwords',
        'get_lemmas_label': 'Get lemmas',
        'delete_numbers_label': 'Delete numbers',
        'save_text': 'Save to file:',
        'file_name_label': 'File name:'
    },
    'sk': {
        'language_picker_label': 'Vyberte si jazyk aplikácie a webovej stránky:',
        'url_label': 'Zadajte URL:',
        'get_links_label': 'Získať odkazy namiesto textu',
        'get_full_links_label': 'Získať iba odkazy s http/https',
        'keyword_input_label': '[Voliteľné] Zadajte hľadané kľúčové slovo:',
        'get_dynamic_content_label': 'Stránka je dynamická',
        'pagination_scrape_label': 'Stránkovanie',
        'pagination_count_label': 'Zadajte počet stránok na zbieranie',
        'clean_stopwords_label': 'Vyčistiť stopwords',
        'get_lemmas_label': 'Lematizácia',
        'delete_numbers_label': 'Vymazať čísla',
        'save_text': 'Uložiť do súboru:',
        'file_name_label': 'Názov súboru:'
    }
}
var optionTexts = {
    'en': {
        'main': 'Full text',
        'p': 'Text in p tags',
        'div': 'Text in div tags',
        'span': 'Text in span tags',
        'ul': 'Text in ul tags',
        'ol': 'Text in ol tags',
        'li': 'Text in li tags',
        'h1': 'H1',
        'h2': 'H2',
        'h3': 'H3',
        'h4': 'H4',
        'h5': 'H5',
        'b': 'Bold',
        'i': 'Italics',
        'a': 'Links'
    },
    'sk': {
        'main': 'Plný text',
        'p': 'Text v značkách p',
        'div': 'Text v značkách div',
        'span': 'Text v značkách span',
        'ul': 'Text v značkách ul',
        'ol': 'Text v značkách ol',
        'li': 'Text v značkách li',
        'h1': 'H1',
        'h2': 'H2',
        'h3': 'H3',
        'h4': 'H4',
        'h5': 'H5',
        'b': 'Tučné',
        'i': 'Kurzíva',
        'a': 'Odkazy'
    }
};
var buttonTexts = {
    'en': {
        'scrape': 'Scrape',
        'save': 'Save to location'
    },
    'sk': {
        'scrape': 'Dolovať',
        'save': 'Uložiť'
    }
}

window.onload = function() {
    changeLanguage();
};

document.getElementById('content_type').onchange = function () {
    checkVisibility();
}

document.getElementById('get_links').onchange = function () {
    checkVisibility();
}
function checkVisibility() {
    var selected_option = document.getElementById('content_type');
    var get_links = document.getElementById('get_links');
    var get_links_label = document.getElementById('get_links_label');
    var get_full_links = document.getElementById('get_full_links');
    var get_full_links_label = document.getElementById('get_full_links_label');
    var searched_keyword = document.getElementById('keyword_input');
    var searched_keyword_label = document.getElementById('keyword_input_label');

    if (selected_option.value == 'a') {
        get_links.classList.remove('hidden');
        get_links_label.classList.remove('hidden');
        if (get_links.checked) {
            get_full_links.classList.remove('hidden');
            get_full_links_label.classList.remove('hidden');
        } else {
            get_full_links.classList.add('hidden');
            get_full_links_label.classList.add('hidden');
        }

    }
    else {
        get_links.classList.add('hidden');
        get_links_label.classList.add('hidden');
        get_full_links.classList.add('hidden');
        get_full_links_label.classList.add('hidden');
    }
    
}
document.addEventListener('DOMContentLoaded', function () {
    var paginationCheckbox = document.getElementById('pagination_scrape');
    var dynamicContent = document.getElementById('get_dynamic_content');
    var countInput = document.getElementById('pagination_count');

    paginationCheckbox.disabled = true;
    countInput.disabled = true;

    dynamicContent.addEventListener('change', function () {
        paginationCheckbox.disabled = !this.checked;
        countInput.disabled = !this.checked || !paginationCheckbox.checked;
        if (this.checked) {
            paginationCheckbox.checked = false;
        }
    });

    paginationCheckbox.addEventListener('change', function () {
        countInput.disabled = !this.checked || !dynamicContent.checked;
    });
});

function showLoading() {
    document.getElementById('loader_overlay').style.display = 'block';
    document.getElementById('loader').style.display = 'block';
}
function hideLoading() {
    document.getElementById('loader_overlay').style.display = 'none';
    document.getElementById('loader').style.display = 'none';
}
document.querySelector('form').addEventListener('submit', function () {
    showLoading();
});
window.addEventListener('load', function () {
    hideLoading();
});

function changeLanguage() {
    var selectedLanguage = document.getElementById('language_picker').value;
    var selectedLabels = labelTexts[selectedLanguage];

    var contentType = document.getElementById('content_type');
    var selectedOptions = optionTexts[selectedLanguage];
    var options = contentType.options;

    var scrapeButton = document.querySelector(".form-container button[type='submit']");
    var saveButton = document.querySelector(".output-form-container button[type='submit']");

    var selectedButtons = buttonTexts[selectedLanguage];

    for (var labelId in selectedLabels) {
        if (selectedLabels.hasOwnProperty(labelId)){
            var pickedLabel = document.getElementById(labelId);
            if (pickedLabel) {
                pickedLabel.textContent = selectedLabels[labelId];
            }
        }
    }
    for (var i = 0; i < options.length; i++) {
        var value = options[i].value;
        if (selectedOptions.hasOwnProperty(value)) {
            options[i].text = selectedOptions[value];
        }
    }
    if (scrapeButton && selectedButtons['scrape']) {
        scrapeButton.textContent = selectedButtons['scrape'];
    }
    if (saveButton && selectedButtons['save']) {
        saveButton.textContent = selectedButtons['save'];
    }
}