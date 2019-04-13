import React, { Component } from 'react';
import { Box, Keyboard } from 'grommet';

import Header from './components/Header';
import Editor from './components/Editor';
import Preview from './components/Preview';
import DiffPreview from './components/DiffPreview';
import History from './components/History';

import { postVersion, fetchHistory } from './services/versionService';

class App extends Component {
  state = {
    text: '',
    activeVersionId: null,
    previousVersionId: null,
    history: []
  }

  async componentDidMount() {
    const history = await fetchHistory()
    this.setState({ history })
  }

  handleEditorTextChange = editedText => {
    this.setState({ text: editedText })
  }

  handleClickHistoryItem = clickedId => {
    const clickedVersionIndex = this.state.history.findIndex(
      ({ _id }) => _id === clickedId
    )
    if (clickedVersionIndex === this.state.history.length - 1) {
      this.setState({
        activeVersionId: clickedId,
        previousVersionId: clickedId
      })
    } else {
      this.setState({
        activeVersionId: clickedId,
        previousVersionId: this.state.history[clickedVersionIndex + 1]._id
      })
    }
  }

  postVersion = async () => {
    await postVersion(this.state.text, 'Author')
    setTimeout(async () => {
      const history = await fetchHistory()
      this.setState({ history })
    }, 2000)
  }

  render() {
    return (
      <Keyboard
        onTab={this.postVersion}
        target='document'
      >
        <Box>
          <Header />
          <Box direction='row' fill='vertical'>
            {this.state.activeVersionId ? (
              <DiffPreview
                versionId={this.state.activeVersionId}
                previousVersionId={this.state.previousVersionId}
              />
            ) : (
              <React.Fragment>
                <Editor
                  text={this.state.text}
                  onChangeText={this.handleEditorTextChange}
                />
                <Preview rawText={this.state.text} />
              </React.Fragment>
            )}
            <History
              history={this.state.history}
              onClickItem={this.handleClickHistoryItem}
              />
          </Box>
        </Box>
      </Keyboard>
    );
  }
}

export default App;
