        let mediaRecorder;
        let audioChunks = [];
        let recordingInterval;
        let recordingStartTime;

        // DOM Elements
        const startBtn = document.getElementById('start');
        const stopBtn = document.getElementById('stop');
        const downloadLink = document.getElementById('download');
        const recordingStatus = document.getElementById('recordingStatus');
        const recordingTime = document.getElementById('recordingTime');
        const fileInput = document.getElementById('file-input');
        const fileInputWrapper = document.querySelector('.file-input-wrapper');
        const fileInputLabel = document.querySelector('.file-input-label');
        const selectedFileDiv = document.querySelector('.selected-file');
        const fileName = document.querySelector('.file-name');
        const fileSize = document.querySelector('.file-size');
        const removeFileBtn = document.querySelector('.remove-file');
        const fileText = document.querySelector('.file-text');
        const form = document.getElementById('voiceForm');
        const summaryOutput = document.getElementById('summaryOutput');

        // Initialize MediaRecorder
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    downloadLink.href = audioUrl;
                    downloadLink.classList.remove('hidden');
                    
                    // Create file for form submission
                    const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    fileInput.files = dataTransfer.files;
                    showSelectedFile(file);
                    
                    audioChunks = [];
                };
            })
            .catch(error => {
                console.error('Mikrofon erişimi reddedildi:', error);
                alert('Mikrofon erişimi için izin vermeniz gerekiyor.');
            });

        // Recording functions
        startBtn.onclick = () => {
            if (mediaRecorder && mediaRecorder.state === 'inactive') {
                mediaRecorder.start();
                startBtn.disabled = true;
                stopBtn.disabled = false;
                recordingStatus.classList.remove('hidden');
                downloadLink.classList.add('hidden');
                
                recordingStartTime = Date.now();
                recordingInterval = setInterval(updateRecordingTime, 1000);
            }
        };

        stopBtn.onclick = () => {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                startBtn.disabled = false;
                stopBtn.disabled = true;
                recordingStatus.classList.add('hidden');
                clearInterval(recordingInterval);
            }
        };

        function updateRecordingTime() {
            const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            recordingTime.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }

        // File upload handlers
        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                showSelectedFile(file);
            }
        });

        removeFileBtn.addEventListener('click', function () {
            fileInput.value = '';
            hideSelectedFile();
        });

        // Drag and drop handlers
        fileInputLabel.addEventListener('dragover', function (e) {
            e.preventDefault();
            fileInputLabel.classList.add('drag-over');
        });

        fileInputLabel.addEventListener('dragleave', function (e) {
            e.preventDefault();
            fileInputLabel.classList.remove('drag-over');
        });

        fileInputLabel.addEventListener('drop', function (e) {
            e.preventDefault();
            fileInputLabel.classList.remove('drag-over');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                showSelectedFile(files[0]);
            }
        });

        function showSelectedFile(file) {
            fileInputWrapper.classList.add('has-file');
            selectedFileDiv.classList.remove('hidden');
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileText.innerHTML = '<p class="text-sm font-medium text-green-600">Ses dosyası seçildi ✓</p>';
        }

        function hideSelectedFile() {
            fileInputWrapper.classList.remove('has-file');
            selectedFileDiv.classList.add('hidden');
            fileText.innerHTML = '<p class="text-lg font-medium text-gray-700 mb-1">Ses dosyası seçmek için tıklayın</p><p class="text-sm text-gray-500">veya dosyayı buraya sürükleyin</p>';
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }