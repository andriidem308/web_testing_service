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

document.addEventListener('DOMContentLoaded', () => {
    "use strict";
    initStudentsTable(studentsTableOptions);
});