import React from 'react';
import './App.css';
import {
	BrowserRouter as Router,
	Route,
	Switch
} from "react-router-dom";
import Register from './components/authentication/Register';
import Login from './components/authentication/Login';
import Home from './components/home/Home';

function App() {
	return (
		<Router>
			<Switch>
				<Route path="/" exact component={Home} />
				<Route path="/login" exact component={Login} />
				<Route path="/register" exact component={Register} />
			</Switch>
		</Router>
	);
}

export default App;
