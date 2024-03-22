/*jshint esversion: 6 */
/*globals $:false */

/*globals console:false */

// function createTestFileTile(rawFilename, clearFilename) {
//     "use strict";
//
//     const selectedFiles = document.getElementById('selectedFiles');
//     const testFileTile = document.createElement('a');
//
//     testFileTile.textContent = clearFilename;
//
//     testFileTile.classList.add('pretty-button');
//     testFileTile.classList.add('dark');
//
//     testFileTile.setAttribute('target', '_blank');
//     testFileTile.setAttribute('href', rawFilename);
//     testFileTile.setAttribute('id', 'test_file_content');
//
//     selectedFiles.appendChild(testFileTile);
// }
//
// function displayFileName() {
//     "use strict";
//
//     const testFileInput = document.getElementById('id_test_file');
//
//     if (testFileInput.files.length > 0) {
//         const oldTestFile = document.getElementById('test_file_content');
//
//         if (oldTestFile) {
//             oldTestFile.remove();
//         }
//
//         const clearFilename = testFileInput.files[0].name;
//         const rawFilename = '/media/problems/test_files/' + clearFilename;
//
//         createTestFileTile(rawFilename, clearFilename);
//     }
// }
//
// function testFileService() {
//
//     const selectedFiles = document.getElementById('selectedFiles');
//     const testFileInput = document.getElementById('id_test_file');
//
//     if (testFileInput) {
//         testFileInput.style.display = 'none';
//
//         const oldTestFile = document.querySelector('#selectedFiles a');
//         const oldTestFileName = document.getElementById('oldTestFileName');
//
//         selectedFiles.innerHTML = selectedFiles.innerHTML.replace(/Currently:.*Change:/s, '');
//         if (oldTestFile) {
//             const rawFilename = oldTestFile.getAttribute('href');
//             const clearFilename = oldTestFileName.getAttribute('content');
//
//             createTestFileTile(rawFilename, clearFilename);
//         }
//     }
// }
//
// testFileService();
//
//
// document.addEventListener('DOMContentLoaded', () => {
//     "use strict";
//
//     let testFileInput = document.getElementById('id_test_file');
//     if (testFileInput) {
//         testFileInput.addEventListener('change', displayFileName);
//     }
// });

