
/* ==========================================
   FILE: js/data/mining-sites.js
   Sample mining sites data
   ========================================== */

const MINING_SITES = [
    {
        id: 1,
        name: "Jharia Coal Mine",
        location: [23.7957, 86.4304],
        status: "active",
        area: 12.5,
        depth: 45.2,
        volume: 2.3,
        type: "Coal",
        operator: "BCCL",
        illegal: false,
        coordinates: [[23.795, 86.430], [23.798, 86.433], [23.796, 86.436], [23.793, 86.434], [23.792, 86.431]]
    },
    {
        id: 2,
        name: "Bailadila Iron Mine",
        location: [18.6294, 81.2849],
        status: "active",
        area: 8.3,
        depth: 62.8,
        volume: 3.1,
        type: "Iron Ore",
        operator: "NMDC",
        illegal: false,
        coordinates: [[18.628, 81.283], [18.631, 81.286], [18.630, 81.289], [18.627, 81.287], [18.626, 81.284]]
    },
    {
        id: 3,
        name: "Kolar Gold Fields",
        location: [12.9565, 78.2690],
        status: "inactive",
        area: 15.7,
        depth: 89.4,
        volume: 4.5,
        type: "Gold",
        operator: "BGML (Closed)",
        illegal: false,
        coordinates: [[12.955, 78.268], [12.958, 78.271], [12.957, 78.273], [12.954, 78.271], [12.953, 78.269]]
    },
    {
        id: 4,
        name: "Illegal Sand Mining Site",
        location: [25.5941, 85.1376],
        status: "illegal",
        area: 0.8,
        depth: 12.3,
        volume: 0.2,
        type: "Sand",
        operator: "Unknown",
        illegal: true,
        coordinates: [[25.593, 85.137], [25.594, 85.138], [25.594, 85.139], [25.593, 85.138]]
    },
    {
        id: 5,
        name: "Panna Diamond Mine",
        location: [24.7180, 80.0785],
        status: "active",
        area: 6.2,
        depth: 38.6,
        volume: 1.8,
        type: "Diamond",
        operator: "NMDC",
        illegal: false,
        coordinates: [[24.717, 80.077], [24.719, 80.079], [24.718, 80.081], [24.716, 80.080], [24.715, 80.078]]
    },
    {
        id: 6,
        name: "Zawar Zinc Mine",
        location: [24.3509, 73.7120],
        status: "active",
        area: 9.8,
        depth: 55.7,
        volume: 2.9,
        type: "Zinc",
        operator: "Hindustan Zinc",
        illegal: false,
        coordinates: [[24.350, 73.711], [24.352, 73.713], [24.351, 73.715], [24.349, 73.714], [24.348, 73.712]]
    },
    {
        id: 7,
        name: "Illegal Quarry Site",
        location: [26.8467, 80.9462],
        status: "illegal",
        area: 1.2,
        depth: 8.5,
        volume: 0.1,
        type: "Stone",
        operator: "Unknown",
        illegal: true,
        coordinates: [[26.846, 80.945], [26.847, 80.947], [26.846, 80.948], [26.845, 80.946]]
    },
    {
        id: 8,
        name: "Singareni Coal Mine",
        location: [18.4386, 79.4192],
        status: "active",
        area: 18.4,
        depth: 72.3,
        volume: 5.2,
        type: "Coal",
        operator: "SCCL",
        illegal: false,
        coordinates: [[18.437, 79.418], [18.440, 79.421], [18.439, 79.423], [18.436, 79.421], [18.435, 79.419]]
    },
    {
        id: 9,
        name: "Kudremukh Iron Mine",
        location: [13.1341, 75.2537],
        status: "inactive",
        area: 11.3,
        depth: 48.9,
        volume: 3.7,
        type: "Iron Ore",
        operator: "KIOCL (Closed)",
        illegal: false,
        coordinates: [[13.133, 75.252], [13.135, 75.255], [13.134, 75.257], [13.132, 75.255], [13.131, 75.253]]
    },
    {
        id: 10,
        name: "Malanjkhand Copper Mine",
        location: [22.0217, 80.7221],
        status: "active",
        area: 7.6,
        depth: 41.2,
        volume: 2.1,
        type: "Copper",
        operator: "HCL",
        illegal: false,
        coordinates: [[22.020, 80.721], [22.023, 80.724], [22.022, 80.726], [22.019, 80.724], [22.018, 80.722]]
    }
];

// Make sites data globally available
window.MINING_SITES_DATA = MINING_SITES;

