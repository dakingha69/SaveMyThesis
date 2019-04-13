import React, { useEffect, useState } from 'react';
import { Box, Heading, Paragraph, Text } from 'grommet';
import ReactDiffViewer from 'react-diff-viewer';
import ReactLoading from 'react-loading';

import { fetchVersion } from '../services/versionService';

const DiffPreview = ({ versionId, previousVersionId }) => {
  const [ fetching, setFetching ] = useState(true)
  const [ activeVersion, setActiveVersion ] = useState({})
  const [ previousVersion, setPreviousVersion ] = useState({})

  const fetchActiveVersion = async () => {
    setFetching(true)
    const fetchedActiveVersion = await fetchVersion(versionId)
    setActiveVersion(fetchedActiveVersion)
    setFetching(false)
  }

  const fetchPreviousVersion = async () => {
    setFetching(true)
    const fetchedPreviousVersion = previousVersionId
      ? await fetchVersion(previousVersionId)
      : {}
    setPreviousVersion(fetchedPreviousVersion)
    setFetching(false)
  }

  useEffect(() => {
    fetchActiveVersion()
    fetchPreviousVersion()
  }, [versionId, previousVersionId])

  return (
    <Box
      pad='medium'
      fill='vertical'
      width='80%'
    >
      {fetching ? (
        <Box
          justify='center'
          align='center'
          direction='row'
          fill
        >
          <ReactLoading
            type='spin'
            color='#7D4CDB'
            height='150px'
            width='150px'
          />
        </Box>
      ) : (
        <Box
          border='all'
          fill='vertical'
          pad='medium'
          overflow='scroll'
        >
          <Heading level={3}>
            {activeVersion.commitTitle}
            <Text weight='normal'>
              {` - ${new Date(activeVersion.timestamp).toDateString()} by ${activeVersion.author}`}
            </Text>
          </Heading>
          <Text>{activeVersion.commitText}</Text>
          <Paragraph />
          <ReactDiffViewer
            oldValue={previousVersion.text}
            newValue={activeVersion.text}
          />
        </Box>
      )}
    </Box>
  );
}
 
export default DiffPreview;