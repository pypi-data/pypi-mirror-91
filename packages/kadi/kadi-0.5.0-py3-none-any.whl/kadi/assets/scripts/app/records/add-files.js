/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import CanvasPainter from 'scripts/lib/components/CanvasPainter.vue';
import UploadManager from 'scripts/lib/components/UploadManager.vue';

new Vue({
  el: '#vm',
  components: {
    CanvasPainter,
    UploadManager,
  },
  data: {
    filename: '',
    currentFile: null,
    imageUrl: null,
    unsavedChanges: false,
    renderDrawingTab: false,
  },
  methods: {
    changeTab(id) {
      // If we render the drawing component before it is shown, its size cannot be initialized correctly.
      if (id === 'upload-drawing') {
        this.renderDrawingTab = true;
      }
    },
    uploadComplete(file) {
      // Note that the current file is also updated when uploading it normally.
      if (this.currentFile && this.currentFile.id === file.id) {
        this.currentFile = file;
      }
    },
    dataURLtoFile(dataurl, filename) {
      const bstr = atob(dataurl.split(',')[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);

      while (n) {
        u8arr[n - 1] = bstr.charCodeAt(n - 1);
        n -= 1;
      }
      return new File([u8arr], filename);
    },
    saveCanvas(canvas) {
      let filename = this.filename;
      if (!filename.endsWith('.png')) {
        filename += '.png';
      }

      const _uploadImage = () => {
        const file = this.dataURLtoFile(canvas.toDataURL(), filename);
        this.$refs.navTabs.changeTab('upload-files');
        this.$refs.uploadManager.addFile(file);

        this.unsavedChanges = false;
      };

      if (this.currentFile && this.currentFile.name === filename) {
        axios.get(this.currentFile._links.self)
          .then((response) => {
            // Check if the content of the current file has changed since loading it by just comparing the checksums.
            if (this.currentFile.checksum !== response.data.checksum) {
              if (confirm(i18n.t('warning.fileChanged'))) {
                _uploadImage();
              }
            } else {
              _uploadImage();
            }
          });
      } else {
        _uploadImage();
      }
    },
  },
  mounted() {
    if (kadi.js_resources.current_file_endpoint) {
      axios.get(kadi.js_resources.current_file_endpoint)
        .then((response) => {
          this.currentFile = response.data;

          if (['image/png', 'image/jpeg'].includes(this.currentFile.magic_mimetype)) {
            this.imageUrl = this.currentFile._links.download;
            this.filename = this.currentFile.name;
            this.$refs.navTabs.changeTab('upload-drawing');
          }
        })
        .catch((error) => kadi.alert(i18n.t('error.loadFile'), {xhr: error.request}));
    }
  },
});
