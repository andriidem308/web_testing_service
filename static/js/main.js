/*jshint esversion: 6 */
/*globals $:false */

/*globals console:false */

const studentsTableOptions = {
    processing: true,
    serverSide: true,
    ajax: {
        url: $('#students-table').data('url'),
        pagingType: "full",
        type: 'GET'
    },
    columns: [
        {data: 'first_name'},
        {data: 'last_name'},
        {data: 'score_percentage'},
        {data: 'problems_solved'},
    ],
    dom: 'Bfrtip',
    iDisplayLength: 15,
};

const initStudentsTable = function (options) {
    "use strict";

    $('#students-table').DataTable().clear().destroy();
    const studentsTable = $('#students-table').DataTable(options);
};

function showDeleteConfirmation() {
    "use strict";

    document.getElementById("disabled-area").classList.add('active');
    document.getElementById("delete-confirmation").classList.add('active-flex');
}

function closeDeleteConfirmation() {
    "use strict";

    document.getElementById("disabled-area").classList.remove('active');
    document.getElementById("delete-confirmation").classList.remove('active-flex');
}

// ----------------------------------------------------------------


function log(str) {"use strict"; console.log(str);}


$(function () {
    $("#id_deadline").datetimepicker({
        format: 'Y-m-d H:00:00',
    });
});


function displayFileName() {
    "use strict";

    const selectedFiles = document.getElementById('selectedFiles');
    const testFileInput = document.getElementById('id_test_file');

    if (testFileInput.files.length > 0) {
        const oldTestFile = document.getElementById('test_file_content');

        if (oldTestFile) {
            oldTestFile.remove();
        }

        const clearFilename = testFileInput.files[0].name;
        const rawFilename = '/media/problems/test_files/' + clearFilename;

        const testFileTile = document.createElement('a');
        testFileTile.textContent = clearFilename;
        testFileTile.classList.add('pretty-button');
        testFileTile.classList.add('dark');
        testFileTile.setAttribute('href', rawFilename);
        testFileTile.setAttribute('download', clearFilename);
        testFileTile.setAttribute('id', 'test_file_content');

        selectedFiles.appendChild(testFileTile);
    }
}

function testFileService() {
    "use strict";

    const selectedFiles = document.getElementById('selectedFiles');
    const testFileInput = document.getElementById('id_test_file');

    if (testFileInput) {
        testFileInput.style.display = 'none';
        testFileInput.setAttribute('onchange', 'displayFileName()');

        const oldTestFile = document.querySelector('#selectedFiles a');
        selectedFiles.innerHTML = selectedFiles.innerHTML.replace(/Currently:.*Change:/s, '');
        if (oldTestFile) {
            const rawFilename = oldTestFile.getAttribute('href');
            const clearFilename = rawFilename.split('/').pop().split('?')[0];
            const oldTestFileTile = document.createElement('a');
            oldTestFileTile.textContent = clearFilename;
            oldTestFileTile.classList.add('pretty-button');
            oldTestFileTile.classList.add('dark');
            oldTestFileTile.setAttribute('href', rawFilename);
            oldTestFileTile.setAttribute('download', clearFilename);
            oldTestFileTile.setAttribute('id', 'test_file_content');

            selectedFiles.appendChild(oldTestFileTile);
        }
    }
}

testFileService();

document.addEventListener('DOMContentLoaded', () => {
    "use strict";
    initStudentsTable(studentsTableOptions);

    (document.querySelectorAll('input, textarea, select') || []).forEach(($trigger) => {
        $trigger.addEventListener('focus', () => {
            $trigger.classList.remove('danger-outline');
        });
    });

    (document.querySelectorAll('label') || []).forEach(($trigger) => {
        $trigger.addEventListener('click', () => {
            $trigger.classList.remove('danger-outline');
        });
    });
});