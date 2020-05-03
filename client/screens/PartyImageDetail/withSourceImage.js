import RestHook from '@unrest/react-rest-hook'

export default RestHook(
  '/api/server/SourceImage/${match.params.sourceimage_id}/',
)
