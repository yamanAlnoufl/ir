import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Search App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: SearchPage(),
    );
  }
}

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});

  @override
  _SearchPageState createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  final TextEditingController _queryController = TextEditingController();
  List _results = [];
  List _refinedQueries = [];
  bool _isLoading = false;
  String _error = '';
  List _suggestions = [];
  String _selectedDataset = '1'; // Default dataset
  Future<void> _setDataset() async {
    try {
      final response = await http.post(
        Uri.parse('http://192.168.252.207:8080/set_dataset'),
        body: {'dataset': _selectedDataset},
      );

      if (response.statusCode == 200) {
        print('Dataset set successfully.');
      } else {
        setState(() {
          _error = 'Error: ${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error: $e';
      });
    }
  }
  Future<void> _getSuggestions(String input) async {
    if (input.isEmpty) {
      setState(() {
        _suggestions = [];
      });
      return;
    }

    try {
      final response = await http.post(
        Uri.parse('http://192.168.252.207:8080/refine_query'),
        body: {'keyword': input},
      );

      if (response.statusCode == 200) {
        setState(() {
          _suggestions = json.decode(response.body)['suggestions'];
        });
      } else {
        setState(() {
          _error = 'Error: ${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error: $e';
      });
    }
  }
  Future<void> _searchQuery() async {
    setState(() {
      _isLoading = true;
      _error = '';
    });

    try {
      final response = await http.post(
        Uri.parse('http://192.168.252.207:8080/get_query'),

        body: {'kewword': _queryController.text},
      );
print(_queryController.text);
      if (response.statusCode == 200) {
        final responseData = json.decode(response.body);
        setState(() {
          _results = responseData['data'];
          _refinedQueries = responseData['suggested_queries'];
        });
      } else {
        setState(() {
          _error = 'Error: ${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }



  Widget _buildResults() {
    if (_results.isEmpty) {
      return const Text('No results found.');
    }
    return ListView.builder(
      itemCount: _results.length,
      itemBuilder: (context, index) {
        final result = _results[index];
        return ListTile(
          title: Text(result['title']),
          subtitle: Text(result['abstract']),
        );
      },
    );
  }

  Widget _buildSuggestions() {
    if (_suggestions.isEmpty) {
      return Container();
    }
    return Column(
      children: _suggestions.map((suggestion) {
        return ListTile(
          title: Text(suggestion),
          onTap: () {
            _queryController.text = suggestion;
            _searchQuery();
          },
        );
      }).toList(),
    );
  }

  Widget _buildRefinedQueries() {
    if (_refinedQueries.isEmpty) {
      return Container();
    }
    return Column(
      children: _refinedQueries.map((query) {
        return ElevatedButton(
          onPressed: () {
            _queryController.text = query;
            _searchQuery();
          },
          child: Text(query),
        );
      }).toList(),
    );
  }
  @override
  void initState() {
    super.initState();
    _setDataset(); // Set the default dataset when the app starts
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Search App'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              children: [
                const Text('Select Dataset: '),
                DropdownButton<String>(
                  value: _selectedDataset,
                  items: [
                    DropdownMenuItem(
                      value: '1',
                      child: const Text('Dataset 1'),
                    ),
                    DropdownMenuItem(
                      value: '2',
                      child: const Text('Dataset 2'),
                    ),
                  ],
                  onChanged: (value) {
                    setState(() {
                      _selectedDataset = value!;
                    });
                    _setDataset(); // Set the selected dataset
                  },
                ),
              ],
            ),
            const SizedBox(height: 10),
            TextField(
              onChanged: _getSuggestions,
              controller: _queryController,
              decoration: InputDecoration(
                hintText: 'Enter your query',
              ),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                ElevatedButton(
                  onPressed: _isLoading ? null : _searchQuery,
                  child: _isLoading ? const CircularProgressIndicator() : const Text('Search'),
                ),
                const SizedBox(width: 10),
              ],
            ),
            const SizedBox(height: 20),
            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : _buildResults(),
            ),
            _buildRefinedQueries(),
            _buildSuggestions(),
          ],
        ),
      ),
    );
  }
}
