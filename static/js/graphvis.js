
/**
 * Uses JQuery to post an ajax request on Neo4j REST API
 */
function restGet() {
    pathname_splitted = window.location.pathname.split('/')
    pigeon_id = pathname_splitted[pathname_splitted.length-1]
    if (document.getElementById('only-ancestors-toggle').checked) {
        only_ancestors = true
    } else {
        only_ancestors = false
    }
    return $.ajax({
                  type: "GET",
                  url: "http://127.0.0.1:5000/api/get-neograph-pigeon",
                  data: {'pigeonID': pigeon_id, 'only_ancestors': only_ancestors}
                  });
}

/**
 * Function to call to display a new graph.
 */
function displayGraph() {

    // Get Cypher query to return node and relations and return results as graph.
    restGet().done(function (data) {

                     // Parse results and convert it to vis.js compatible data.
                     var graphData = parseGraphResultData(data);
                     var nodes = convertNodes(graphData.nodes);
                     var edges = convertEdges(graphData.edges);
                     var visData = {
                     nodes: nodes,
                     edges: edges
                     };

                     displayVisJsData(visData);
                     });
}

function displayVisJsData(data) {
    var container = document.getElementById('vis');

    var options = {
        nodes: {
            shape: 'circle',
            size : 50,

            font : {
                size : 20,
                color : '#ffffff'
            },
            borderWidth : 2
        },
        edges: {
            arrows: 'to',
            length: 300
        }
    };

    // initialize the network!
    var network = new vis.Network(container, data, options);

}

function parseGraphResultData(data) {
    var nodes = {}, edges = {};
    data.results[0].data.forEach(function (row) {
                                 row.graph.nodes.forEach(function (n) {
                                                         if (!nodes.hasOwnProperty(n.id)) {
                                                         nodes[n.id] = n;
                                                         }
                                                         });

                                 row.graph.relationships.forEach(function (r) {
                                                                 if (!edges.hasOwnProperty(r.id)) {
                                                                 edges[r.id] = r;
                                                                 }
                                                                 });
                                 });

    var nodesArray = [], edgesArray = [];

    for (var p in nodes) {
        if (nodes.hasOwnProperty(p)) {
            nodesArray.push(nodes[p]);
        }
    }

    for (var q in edges) {
        if (edges.hasOwnProperty(q)) {
            edgesArray.push(edges[q])
        }
    }

    return {nodes: nodesArray, edges: edgesArray};
}

function convertNodes(nodes) {
    var convertedNodes = [];
    pathname_splitted = window.location.pathname.split('/')
    pigeon_id = pathname_splitted[pathname_splitted.length-1]
    nodes.forEach(function (node) {
                  var nodeLabel = 'Pigeon'
                  var displayedLabel = node.properties['cislo_krouzku'] + '/' + node.properties['rocnik'];
                  if(node.properties['pohlavi'] == 0.1) {
                      color = '#f5a2ec'
                  } else {
                      color = '#97C2FC'
                  }
                  if(node.properties['id'] == pigeon_id) {
                      borderWidth = 5
                  } else {
                      borderWidth = 1
                  }
                  convertedNodes.push({
                                      id: node.id,
                                      label: displayedLabel,
                                      group: nodeLabel,
                                      color: color,
                                      borderWidth: borderWidth
                                      })
                  });

    return convertedNodes;
}

function convertEdges(edges) {
    var convertedEdges = [];

    edges.forEach(function (edge) {
                  convertedEdges.push({
                                      from: edge.startNode,
                                      to: edge.endNode,
                                      label: edge.type
                                      })
                  });

    return convertedEdges;
}

displayGraph()
