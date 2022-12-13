import './App.css';
import Navbar from "./components/Navbar";
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Switch } from 'react-router-dom';
import Home from './components/pages/Home';
import Descriptions from './components/pages/Descriptions';
import Footer from './components/Footer'
import Docs from './components/pages/Documentation';
import Experiment from './components/pages/ExperimentMain';
// import ExpTools from './components/pages/Single-Tool';
// import ExpSF from './components/pages/Single-Field';
// import ExpStep from './components/pages/Stepped-Field';
// import ExpSLIMpage from './components/pages/SLIM';


// function App() {
//   return (
//     <>
//       <Router>
//         <Navbar />
//         <Home>
//         </Home>
//           <Routes>
//           </Routes>
//       </Router>
//     </>
//   );
// }

// export default App;

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route exact path= '/' exact element={<Home />} />
          <Route exact path= '/Descriptions' exact element={<Descriptions />} />
          <Route exact path= '/Documentation' exact element={<Docs />} />
          <Route exact path= '/Experiment' exact element={<Experiment />} />
          {/* <Route exact path= '/Single-Tool' exact element={<ExpTools />} />
          <Route exact path= '/Single-Field' exact element={<ExpSF />} />
          <Route exact path= '/Stepped-Field' exact element={<ExpStep />} />
          <Route exact path= '/SLIM' exact element={<ExpSLIMpage />} /> */}
        </Routes>
        <Footer />
      </Router>
    </>
  );
}

export default App;