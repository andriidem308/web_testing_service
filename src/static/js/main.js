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
        {data: 'tests_solved'},
    ],
    columnDefs: [
        {
            targets: [3, 4],
            className: "text-center",
            width: "10%",
        },
        {
            targets: [2],
            className: "text-center",
        },
    ],
    dom: 'Bfrtip',
    iDisplayLength: 15,
    oLanguage: {
        sEmptyTable: 'No students in this group'
    },
};

const initStudentsTable = function (options) {
    "use strict";

    $('#students-table').DataTable().clear().destroy();
    const studentsTable = $('#students-table').DataTable(options);
};


const testSolutionsTableOptions = {
    processing: true,
    serverSide: true,
    ajax: {
        url: $('#test-solutions-table').data('url'),
        pagingType: "full",
        type: 'GET'
    },
    columns: [
        {data: 'student'},
        {data: 'group'},
        {data: 'score'},
    ],
    columnDefs: [
        {
            targets: [2],
            className: "text-center",
        },
    ],
    dom: 'Bfrtip',
    searching: false,
    paging: false,
    info: false,
    iDisplayLength: 50,
    oLanguage: {
        sEmptyTable: 'No one solved this test'
    },
    scrollY: '235px',
    scrollCollapse: true,
};

const initTestSolutionsTable = function (options) {
    "use strict";

    $('#test-solutions-table').DataTable().clear().destroy();
    const testSolutionsTable = $('#test-solutions-table').DataTable(options);
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

function showArticleDeleteConfirmation(articleID) {
    "use strict";

    document.getElementById("disabled-area").classList.add('active');
    document.getElementById("delete-confirmation-" + articleID).classList.add('active-flex');
}

function closeArticleDeleteConfirmation(articleID) {
    "use strict";

    document.getElementById("disabled-area").classList.remove('active');
    document.getElementById("delete-confirmation-" + articleID).classList.remove('active-flex');
}



// ----------------------------------------------------------------


function log(str) {"use strict"; console.log(str);}


$(function () {
    $("#id_deadline").datetimepicker({
        format: 'Y-m-d H:00:00',
    });
});


function createTestFileTile(clearFilename, downloadURL=null) {

    const selectedFiles = document.getElementById('selectedFiles');
    const testFileTile = document.createElement('a');

    testFileTile.textContent = clearFilename;

    testFileTile.classList.add('pretty-button');
    testFileTile.classList.add('dark');

    if (downloadURL) {
        testFileTile.setAttribute('href', downloadURL);
        testFileTile.setAttribute('download', clearFilename);
    }
    testFileTile.setAttribute('id', 'test_file_content');

    selectedFiles.appendChild(testFileTile);
}


function displayFileName() {
    "use strict";

    const testFileInput = document.getElementById(
        'id_test_file') || document.getElementById('id_attachment');

    if (testFileInput.files.length > 0) {
        const oldTestFile = document.getElementById('test_file_content');

        if (oldTestFile) {
            oldTestFile.remove();
        }

        const clearFilename = testFileInput.files[0].name;

        createTestFileTile(clearFilename);
    }
}

function testFileService() {

    const selectedFiles = document.getElementById('selectedFiles');
    const testFileInput = document.getElementById(
        'id_test_file') || document.getElementById('id_attachment');

    if (testFileInput) {
        testFileInput.style.display = 'none';

        const oldTestFile = document.querySelector('#selectedFiles a');
        selectedFiles.innerHTML = selectedFiles.innerHTML.replace(/Currently:.*Change:/s, '');
        if (oldTestFile) {
            const downloadURL = oldTestFile.getAttribute('href');
            const clearFilename = downloadURL.split('/').pop().split('?')[0];

            createTestFileTile(clearFilename, downloadURL);
        }
    }
}

testFileService();

document.addEventListener('DOMContentLoaded', () => {
    "use strict";
    initStudentsTable(studentsTableOptions);
    initTestSolutionsTable(testSolutionsTableOptions);

    let notifications = document.querySelectorAll('.notification__message');
    notifications.forEach(function (element) {
        element.innerHTML = element.textContent;
    });

    let testFileInput = document.getElementById('id_test_file');
    if (testFileInput) {
        testFileInput.addEventListener('change', displayFileName);
    }

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