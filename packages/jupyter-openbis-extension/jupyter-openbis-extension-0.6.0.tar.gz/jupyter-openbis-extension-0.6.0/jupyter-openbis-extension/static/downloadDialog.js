define([
        "base/js/dialog",
        "jquery",
        "./common",
        "./state",
        //"./entitySearcher"
    ],
    function (dialog, $, common, state) {

        var spinner = document.createElement("IMG")
        spinner.className="openbis-feedback"
        spinner.src=""
        function showSpinner() {
            var userName = window.location.pathname.split("/")[2];
            spinner.src = '/user/' + userName+ '/nbextensions/jupyter-openbis-extension/spinner.gif'
        }
        function hideSpinner() {
            spinner.src=""
        }

        function writeMetaData(data) {
            var notebook = IPython.notebook
            if (typeof notebook.metadata.datasets === 'undefined') {
                notebook.metadata.datasets = {}
            }
            // store metadata about the downloaded files into the notebook-metadata
            if (data.permId) {
                notebook.metadata.datasets[data.permId] = {
                    "permId": data.permId,
                    "path": data.path,
                    "dataStore": data.dataStore,
                    "location": data.location,
                    "size": data.size,
                    "files": data.files,
                    "status": data.statusText
                }
            }
        }

        function show_datasets_table(env, data, datasets_table, pagingContainer, downloadPath, entityIdentifier) {
            var table = document.createElement("TABLE")
            table.className = "table-bordered table-striped table-condensed text-nowrap"
            table.style.width = "100%"

            var thead = table.createTHead()
            var t_row = thead.insertRow()
            var titles = ['', 'permId', 'Name', 'Type', 'Registration Date', 'Status', 'Size']
            titles.forEach(function (title) {
                t_row.insertCell().textContent = title
            })
            var tbody = table.createTBody()

            for (dataSet of data.dataSets) {

                const permId = document.createElement("INPUT")
                permId.type = "checkbox"
                permId.name = "permId"
                permId.value = dataSet.permId
                permId.checked = state.selectedDatasets.has(permId.value)
                permId.onclick = () => permId.checked ? state.selectedDatasets.add(permId.value) : state.selectedDatasets.delete(permId.value)

                var row = tbody.insertRow()
                row.insertCell().appendChild(permId)
                row.insertCell().textContent = dataSet.permId
                row.insertCell().textContent = dataSet['$NAME']
                row.insertCell().textContent = dataSet.type
                row.insertCell().textContent = dataSet.registrationDate
                row.insertCell().textContent = dataSet.status
                row.insertCell().textContent = dataSet.size
            }

            while (datasets_table.firstChild) {
                datasets_table.removeChild(datasets_table.firstChild);
            }
            datasets_table.appendChild(table)
            datasets_table.style.overflow="auto"


            const totalCount = parseInt(data.totalCount)
            const count = parseInt(data.count)
            const startWith = parseInt(data.start_with)
            const hasNext = startWith + count < totalCount
            const hasPrevious = startWith > 0
            const nextCmd = () => getDatasets(env, startWith+5, 5, entityIdentifier, datasets_table, pagingContainer, downloadPath)
            const previousCmd = () => getDatasets(env, startWith-5, 5, entityIdentifier, datasets_table, pagingContainer, downloadPath)

            var previous = document.createElement("A")
            previous.className = "fas fa fa-caret-left fa-2x"
            previous.style.verticalAlign="middle"
            if (hasPrevious) {
                previous.href = "#"
                previous.onclick = previousCmd
            }

            var next = document.createElement("A")
            next.className = "fas fa fa-caret-right fa-2x"
            next.style.verticalAlign = "middle"
            if (hasNext) {
                next.href = "#"
                next.onclick = nextCmd
            }

            var countStr = document.createElement("STRONG")
            var until = startWith + count > totalCount ? totalCount : startWith + count
            var startWithStr = startWith + 1
            countStr.innerHTML = startWithStr + "&ndash;" + until + "/" + totalCount
            countStr.style.paddingLeft = "10px"
            countStr.style.paddingRight = "10px"
            countStr.style.verticalAlign="middle"

            var paging = document.createElement("DIV")
            paging.style.width = "100%"
            paging.appendChild(previous)
            if (hasPrevious) {
                previous.style.color = "inherit"
            }
            else {
                previous.style.color="transparent"
            }
            paging.appendChild(countStr)
            paging.appendChild(next)
            if (hasNext) {
                next.style.color="inherit"
            }
            else {
                next.style.color="transparent"
            }

            while (pagingContainer.firstChild) {
                pagingContainer.removeChild(pagingContainer.firstChild);
            }
            pagingContainer.appendChild(paging)
        }

        function getDatasets(env, startWith, count, entityIdentifier, datasets_table, pagingContainer, downloadPath) {
            var connection_name = state.connection.name
            if (!connection_name) {
                alert('Please choose a connection')
                return false
            }

            currentEntityIdentifier = entityIdentifier.value
            if (!currentEntityIdentifier) {
                alert('Please specify an Entity identifier/permId')
                return false
            }
            var url = env.notebook.base_url 
                + 'openbis/sample/' 
                + connection_name 
                + '/' 
                + encodeURIComponent(currentEntityIdentifier)
                + "?start_with="
                + startWith 
                + "&count="
                + count

            fetch(url)
                .then(function (response) {
                    if (response.ok) {
                        response.json()
                            .then(function (data) {
                                show_datasets_table(env, data, datasets_table, pagingContainer, downloadPath, entityIdentifier)
                            })
                    } else {
                        response.json()
                            .then(function (error) {
                                console.log(error.reason)
                                alert("Error: " + error.reason)
                            })
                    }
                })
                .catch(function (error) {
                    console.error('A serious network problem occured:', error)
                })
        }


        return {
            help: 'Download openBIS datasets',
            icon: 'fa-download',
            help_index: '',
            handler: function (env) {
                console.log(env);
                state.selectedDatasets = new Set([])

                conn_table = document.createElement("DIV")
                conn_table.id = "openbis_connections"

                var showDataSets = document.createElement("DIV")
                var title = document.createElement("STRONG")
                title.textContent = "Entity identifier/permId: "
                showDataSets.appendChild(title)
                showDataSets.style.marginTop = '10px'

                var entityIdentifier = document.createElement("INPUT")
                entityIdentifier.type = "text"
                entityIdentifier.name = "entityIdentifier"
                entityIdentifier.size = 40
                entityIdentifier.placeholder = "Sample or Experiment identifier/permId"
                entityIdentifier.value = state.entityIdentifier ? state.entityIdentifier : ""


                var datasets_table = document.createElement("DIV")
                var pagingContainer = document.createElement("DIV")

                var show_datasets_btn = document.createElement("BUTTON")
                show_datasets_btn.className = "btn-info btn-xs"
                show_datasets_btn.textContent = "show datasets"
                show_datasets_btn.style.margin="10px"

                showDataSets.appendChild(entityIdentifier)
                showDataSets.appendChild(show_datasets_btn)
                showDataSets.appendChild(pagingContainer)
                showDataSets.appendChild(document.createElement('BR'))
                showDataSets.appendChild(datasets_table)

                var dataset_direct = document.createElement("P")
                dataset_direct.style.marginTop = '10px'
                dataset_direct.innerHTML = '<strong>Enter DataSet permId directly: </strong>'

                var datasetPermId = document.createElement("INPUT")
                datasetPermId.type = "text"
                datasetPermId.name = "datasetPermId"
                datasetPermId.size = "40"
                datasetPermId.placeholder = "dataSet permId"

                dataset_direct.appendChild(datasetPermId)

                var downloadPath = document.createElement("INPUT")
                downloadPath.type = "text"
                downloadPath.name = "downloadPath"
                downloadPath.size = "90"
                downloadPath.value = state.download_dir ? state.download_dir : state.working_dir

                show_datasets_btn.onclick =
                    () => getDatasets(env, 0, 5, entityIdentifier, datasets_table, pagingContainer, downloadPath)


                var path = document.createElement("DIV")
                path.innerHTML = "<strong>download data to path: </strong>"
                path.appendChild(downloadPath)

                var download_dialog_box = document.createElement("DIV")

                let mainError = common.createErrorElement()
                if (!state.connection.name) {
                    mainError.textContent = "Please choose a connection first."
                    //mainError.textContent = "Network problem: please check your connection first."
                }
                download_dialog_box.appendChild(mainError)
                download_dialog_box.appendChild(spinner)
                download_dialog_box.appendChild(conn_table)
                download_dialog_box.appendChild(showDataSets)
                download_dialog_box.appendChild(dataset_direct)
                download_dialog_box.appendChild(path)

                function onOk() {
                    state.entityIdentifier = entityIdentifier.value
                    state.directPermId = datasetPermId.value
                    state.download_dir = downloadPath.value
                }

                function onCancel() {
                    state.entityIdentifier = entityIdentifier.value
                    state.directPermId = datasetPermId.value
                }

                function downloadDataset(connection_name, selectedPermIds, downloadPath) {

                    var spinnerCounter = selectedPermIds.length
                    for (permId of selectedPermIds) {
                        var downloadUrl = env.notebook.base_url + 'openbis/dataset/' +
                            connection_name + '/' + permId + '/' + encodeURIComponent(downloadPath)

                        fetch(downloadUrl)
                            .then(function (response) {
                                spinnerCounter = spinnerCounter - 1
                                if (spinnerCounter === 0) {
                                    hideSpinner()
                                    $('div.modal').remove()
                                    $('div.modal-backdrop').remove()
                                }
                                if (response.ok) {
                                    response.json()
                                        .then(function (data) {
                                            common.createFeedback('success', data.statusText)

                                            // successful download:
                                            // write statusText from returned data to notebooks metadata
                                            writeMetaData(data)

                                            // keep current download path for later use
                                            currentDownloadPath = downloadPath
                                        })
                                }
                                else {
                                    response.json()
                                        .then(function (error) {
                                            console.log(error.reason)
                                            alert("Error: " + error.reason)
                                        })
                                }
                            })
                            .catch(function (error) {
                                console.error('A serious network problem occured:', error)
                            })
                    }
                }

                function onDownloadClick() {
                    var selected_conn = state.connection.name
                    if (!selected_conn) {
                        alert('please choose a connection')
                        return false
                    }

                    var selectedPermIds = []
                    for (row of state.selectedDatasets) {
                        selectedPermIds.push(row)
                    }
                    if (datasetPermId.value) {
                        selectedPermIds.push(datasetPermId.value)
                    }
                    if (!selectedPermIds) {
                        alert('please select a dataset or provide a permId')
                        return false
                    }

                    if (!downloadPath.value) {
                        alert('Please specify where you would like to download your files!')
                        return false
                    }

                    downloadDataset(selected_conn, selectedPermIds, downloadPath.value)
                    showSpinner()
                    onOk()
                    return false
                }

                dialog.modal({
                    body: download_dialog_box,
                    title: 'Download openBIS DataSets',
                    buttons: {
                        'Cancel': {
                            click: () => onCancel()
                        },
                        'Download': {
                            class: 'btn-primary btn-large',
                            click: onDownloadClick,
                        }
                    },
                    notebook: env.notebook,
                    keyboard_manager: env.notebook.keyboard_manager
                })
            }
        }
    }
)
