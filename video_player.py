"""A video player class."""

from .video_library import VideoLibrary,VideoLibraryError
from .video_playback import VideoPlayback, VideoPlaybackError, PlaybackState
from .video import FlagError
from . import video_playlist_library
from .video_playlist import VideoPlaylistError
from .video_playlist_library import VideoPlaylistLibraryError


class VideoPlayerError(Exception):
    pass

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlists = video_playlist_library.VideoPlaylistLibrary()
        self._playback = VideoPlayback()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        print("Here's a list of all available videos:")
        for each in self._video_library.get_all_videos():
            print(each)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        try:
            video= self._video_library[video_id]
            video.check_allowed()
        except (VideoLibraryError, FlagError) as e:
            print(f"Cannot play video: {e}")
            return

        if self._playback.state != PlaybackState.STOPPED:
            self.stop_video()
        self._playback.play(video)
        print(f"Playing video: {video.title}")

    def stop_video(self):
        """Stops the current video."""

        try:
            video = self._playback.get_video()
            print(f"Stopping video: {video.title}")
            self._playback.stop()
        except VideoPlaybackError as e:
            print(f"Cannot stop video: {e}")

    def play_random_video(self):
        """Plays a random video from the video library."""

        random_id = self._video_library.get_random_id()
        #print("random id:", random_id)

        if random_id is None:
            print("No videos available")
        else:
            self.play_video(random_id)


    def pause_video(self):
        """Pauses the current video."""

        try:
            video = self._playback.get_video()
        except VideoPlaybackError as e:
            print(f"Cannot pause video: {e}")
            return

        if self._playback.state == PlaybackState.PAUSED:
            print(f"Video already paused: {video.title}")
            return

        print(f"Pausing video: {video.title}")
        self._playback.pause()


    def continue_video(self):
        """Resumes playing the current video."""

        try:
            video = self._playback.get_video()
            self._playback.resume()
            print(f"Continuing video: {video.title}")
        except VideoPlaybackError as e:
            print(f"Cannot continue video: {e}")

    def show_playing(self):
        """Displays video currently playing."""

        if self._playback.state == PlaybackState.PLAYING:
            print(f"Currently playing: {self._playback.get_video()}")
        elif self._playback.state == PlaybackState.PAUSED:
            print(f"Currently playing: {self._playback.get_video()} - PAUSED")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            self._playlists.create(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")
        except VideoPlaylistLibraryError as e:
            print(f"Cannot create playlist: {e}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        try:
            playlist = self._playlists[playlist_name]
            video = self._video_library[video_id]
            video.check_allowed()
            playlist.add_video(video)
            print(f"Added video to {playlist_name}: {video.title}")
        except (VideoPlaylistLibraryError, VideoPlaylistError, VideoLibraryError, FlagError) as e:
            print(f"Cannot add video to {playlist_name}: {e}")

    def show_all_playlists(self):
        """Display all playlists."""

        playlists = list(self._playlists.get_all())

        if not playlists:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        for playlist in playlists:
            print(f"  {playlist}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:        
            playlist = self._playlists[playlist_name]
        except VideoPlaylistLibraryError as e:
            print(f"Cannot show playlist {playlist_name}: {e}")
            return

        print(f"Showing playlist: {playlist_name}")

        if not playlist.videos:
            print("No videos here yet")
            return

        for video in playlist.videos:
            print(f"  {video}")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        try:
            playlist = self._playlists[playlist_name]
            video = self._video_library[video_id]
            playlist.remove_video(video)
            print(f"Removed video from {playlist_name}: {video.title}")
        except (VideoPlaylistError, VideoLibraryError, VideoPlaylistLibraryError) as e:
            print(f"Cannot remove video from {playlist_name}: {e}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:        
            playlist = self._playlists[playlist_name]
            playlist.clear()
            print(f"Successfully removed all videos from {playlist_name}")
        except (VideoPlaylistError, VideoPlaylistLibraryError) as e:
            print(f"Cannot clear playlist {playlist_name}: {e}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:        
            playlist = self._playlists[playlist_name]
            del self._playlists[playlist_name]
            print(f"Deleted playlist: {playlist_name}")
        except VideoPlaylistLibraryError as e:
            print(f"Cannot delete playlist {playlist_name}: {e}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
