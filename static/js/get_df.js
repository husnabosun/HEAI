let test_infoJSON = [];

$.getJSON('/static/files/test_info.json', function (data) {
    test_infoJSON = data;
    initTable();
});

$(document).on('click', '.show-info-btn', function () {
    let info = $(this).data('info');
    let hormone = $(this).data('hormone')
    $('#hormoneName').text(hormone)  
    $('#modalContent').text(info);
    $('#infoModal').removeClass('hidden'); 
});

// Modal kapatma
$('#closeModal').on('click', function () {
    $('#infoModal').addClass('hidden');
});

function normalize(text) {
    return text ? text.trim().replace(/\s+/g, ' ').toLowerCase() : '';
}
