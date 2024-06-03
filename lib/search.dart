import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SearchScreen extends StatefulWidget {
  @override
  _SearchScreenState createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  TextEditingController _controller = TextEditingController();
  List<Map<String, dynamic>> searchResults = [];

  void searchQuery(String query) async {
    String url = 'http://192.168.166.207:5000/get_query';
    Map<String, String> headers = {"Content-type": "application/json"};
    String json = '{"keyword": "$query"}';

    http.Response response = await http.post(url as Uri, headers: headers, body: json);
    if (response.statusCode == 200) {
      print ('hj');
      Map<String, dynamic> data = jsonDecode(response.body);
      setState(() {
        searchResults = List<Map<String, dynamic>>.from(data['data']);
      });
    } else {
      // Handle error
      print('Failed to load search results');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Search'),
      ),
      body: Column(
        children: [
          TextField(
            controller: _controller,
            decoration: InputDecoration(
              labelText: 'Enter your search query',
            ),
            onSubmitted: (value) {
              searchQuery(value);
            },
          ),
          Expanded(
            child: ListView.builder(
              itemCount: searchResults.length,
              itemBuilder: (BuildContext context, int index) {
                return ListTile(
                  title: Text(searchResults[index]['title']),
                  subtitle: Text(searchResults[index]['abstract']),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
