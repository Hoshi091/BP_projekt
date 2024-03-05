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
    if (selected_option.value != 'main') {
        searched_keyword.classList.add('hidden');
        searched_keyword_label.classList.add('hidden');
        searched_keyword.value = "";
    } else {
        searched_keyword.classList.remove('hidden');
        searched_keyword_label.classList.remove('hidden');
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