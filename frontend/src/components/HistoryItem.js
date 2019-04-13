import React from 'react';
import { Box, Text } from 'grommet';
import { AddCircle, Edit, Trash, Radial } from 'grommet-icons';

const ICON_MAP = {
  'change': <Edit />,
  'add': <AddCircle />,
  'remove': <Trash />,
}

const HistoryItem = ({ commitTitle, timestamp, author, onClick }) => {
  const commitPredicate = commitTitle.split(' ')[0].toLowerCase()

  return (
    <Box
      className='pointer'
      direction='row'
      onClick={() => onClick()}
      flex={false}
    >
      <Box
        fill='vertical'
        border={{
          side: 'left',
          color: 'dark-3'
        }}
        justify='center'
        height='small'
        >
        <Box
          style={{
            backgroundColor: 'white',
            marginLeft: '-11px',
          }}
        >
          {ICON_MAP[commitPredicate] || <Radial />}
        </Box>
      </Box>
      <Box pad='small' justify='center'>
        <Text>{commitTitle}</Text>
        <Text size='small'>
          {`${new Date(timestamp).toDateString()} by ${author}`}
        </Text>
      </Box>
    </Box>
  );
}
 
export default HistoryItem;