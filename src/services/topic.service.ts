import { TopicServiceClient } from "./api-client";
import { TopicsResponseSchema } from "./openapi-client";

class TopicService {

  static async getTopics(): Promise<TopicsResponseSchema> {
    try {
      const page = 1;
      const perPage = 5;
      const response = await TopicServiceClient.getTopics(page, perPage);
      return response.data;
    } catch (error) {
      console.error("Error fetching topic", error);
      throw error;
    }
  }
}


export default TopicService