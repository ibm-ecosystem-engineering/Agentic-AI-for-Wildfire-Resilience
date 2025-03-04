    // Function to generate the table
  // Function to create a table
  function createTable(data, tableContainerId) {
    
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    console.log (data)

    // Create table header
    const headerRow = document.createElement("tr");
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement("th");
        th.textContent = key;
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    data.forEach(item => {
        const row = document.createElement("tr");
        Object.values(item).forEach(value => {
            const td = document.createElement("td");
            td.textContent = value;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    // Append table to container
    document.getElementById(tableContainerId).appendChild(table);
}

function createTable2(data, tableContainerId) {
    
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    console.log (data)

    // Create table header
    const headerRow = document.createElement("tr");
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement("th");
        th.textContent = key;
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    data.forEach(item => {
        const row = document.createElement("tr");
        Object.values(item).forEach(value => {
            const td = document.createElement("td");
            td.textContent = value;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    // Append table to container
    document.getElementById(tableContainerId).appendChild(table);
}