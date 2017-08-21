/**
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package tools.descartes.petstore.image.storage.rules;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;
import static org.mockito.Mockito.when;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import tools.descartes.petstore.entities.ImageSize;
import tools.descartes.petstore.image.StoreImage;

public class TestStoreLargeImages {
	
	@Mock
	private StoreImage mockedLargeImg;
	@Mock
	private StoreImage mockedIconImg;
	@Mock
	private StoreImage mockedMainImg;
	@Mock
	private StoreImage mockedPreviewImg;

	@Before
	public void initialize() {
		MockitoAnnotations.initMocks(this);
		when(mockedLargeImg.getSize()).thenReturn(ImageSize.FULL);
		when(mockedIconImg.getSize()).thenReturn(ImageSize.ICON);
		when(mockedMainImg.getSize()).thenReturn(ImageSize.MAIN_IMAGE);
		when(mockedPreviewImg.getSize()).thenReturn(ImageSize.PREVIEW);
	}
	
	@Test
	public void testRule() {
		StoreLargeImages uut = new StoreLargeImages();
		assertTrue(uut.test(mockedLargeImg));
		assertFalse(uut.test(mockedIconImg));
		assertFalse(uut.test(mockedMainImg));
		assertFalse(uut.test(mockedPreviewImg));
	}
	
}